# app/__init__.py
import os

from flask import request, Flask, session, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from models import User
from config import app_config
from controllers import user, book, genre, library, rate

# Authentication
from datetime import timedelta
from models import TokenBlacklist
from blacklist_helpers import (
    is_token_revoked, add_token_to_database,
    revoke_token, prune_database, TokenNotFound
)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies
)

# initialize sql-alchemy
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
api = Api(app)
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy()
db.init_app(app)

# ------------- Authentication  Setup--------
SESSION_TYPE = 'redis'
app.secret_key = 'teamling'
jwt = JWTManager(app)

# setup
ACCESS_EXPIRES = timedelta(minutes=15)
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['JWT_SECRET_KEY'] = 'TeamLing96'


# Define our callback function to check if a token has been revoked or not
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@jwt.expired_token_loader
@jwt.invalid_token_loader
@jwt.revoked_token_loader
@jwt.user_loader_error_loader
@jwt.unauthorized_loader
def my_expired_token_callback(response=None):
    return jsonify({
        "message": "Authentication information is missing or invalid"
    }), 401


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    user = User.query.get(identity)
    return {
        'role': user.role
    }


# # ----------- User API URI -----------

# User login
class Login(Resource):
    def post(self):
        try:
            user = User.query.filter_by(username=request.json['username']).first()
            if user and user.check_password(request.json['password']):
                access_token = create_access_token(identity=user.id)
                # Store the tokens in our store with a status of not currently revoked.
                add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
                return jsonify({'token': access_token})
            else:
                return "Invalid username/password supplied"
        except:
            return "Invalid username/password supplied"


api.add_resource(Login, '/users/login')


# User login
class Logout(Resource):
    @jwt_required
    def post(self):
        user_identity = get_jwt_identity()
        try:
            token = TokenBlacklist.query.filter_by(user_identity=user_identity, revoked=False).first()
            revoke_token(token.id, user_identity)
            response = app.response_class(
                response="OK",
                status=200
            )
            return response
        except TokenNotFound:
            response = app.response_class(
                response="Invalid token",
                status=400
            )
            return response


api.add_resource(Logout, '/users/logout')


# Get Specific User
class Get_User(Resource):
    def get(self, username):
        return user.get_user(username)


api.add_resource(Get_User, '/users/<username>')


# Show list of user
class Get_User_List(Resource):
    # @app.route('/users-list', methods=['GET', 'POST'])
    def get(self):
        return user.users_list()


api.add_resource(Get_User_List, '/users-list')


# Create new User
class Register_User(Resource):
    def post(self):
        # if form.validate_on_submit():
        return user.create_user(request)
        # return content


api.add_resource(Register_User, '/users')


# ------------------------------------

# ----------- Book API URI -----------

# Get all books
class Get_Books(Resource):

    # @app.route('/book', methods=['GET', 'POST'])
    def get(self):
        return book.booklist()

    def post(self):
        return book.add_new_book(request)


api.add_resource(Get_Books, '/book')


# Get Specific Book
class Get_Book(Resource):
    # @app.route('/book/<id>', methods=['GET', 'DELETE'])
    def get(self, id):
        return book.get_book(id)

    def delete(self, id):
        return book.delete_book(id)


api.add_resource(Get_Book, '/book/<id>')


# -------------------------------------

# ----------- Genra API URI -----------

# Get Genre List
class Genre_List(Resource):
    def get(self):
        return genre.genrelist()

    def post(self):
        return genre.add_new_genre(request)


api.add_resource(Genre_List, '/genre')


# Get Specific Genra
class Get_Genra(Resource):
    # @app.route('/genre/<id>', methods=['GET', 'DELETE'])
    def get(self, id):
        return genre.get_genre(id)

    def delete(self, id):
        return genre.delete_genre(id)


api.add_resource(Get_Genra, '/genre/<id>')


# Add book to genra
class Add_Book_Genra(Resource):
    # @app.route('/genre/addbook/<id>', methods=['POST'])
    def post(self, id):
        return genre.add_book_genre(request, id)


api.add_resource(Add_Book_Genra, '/genre/addbook/<id>')


# ---------------------------------------

# ----------- Library API URI -----------

# # User Library
# class User_Library(Resource):
#     # @app.route('/library', methods=['GET', 'POST'])
#     def get(self):
#             return library.get_library(id)
#     def post(self):
#         return genre.add_book_lib(id)
#
#
# api.add_resource(User_Library, '/library')
# ------------------------------------

# ----------- Rate API URI -----------

# # Comment/Rate the book
class Comment_Rate_Book(Resource):
    # @app.route('/rate', methods=['POST'])
    def post(self):
        try:
            user_id = get_jwt_identity()
            if user_id:
                rate_object = request.get_json()
                return rate.rate_and_comment(user_id, rate_object['book_id'], rate_object['rate'],
                                             rate_object['comment'])

        except:
            response = jsonify({"message": "Authentication information is missing or invalid"}), 401
            response.status_code = 401
            return response


#
api.add_resource(Comment_Rate_Book, '/rate')


#
#
# # Get all ratings on the book
# class Get_Ratings(Resource):
# # @app.route('/rate/<book_id>', methods=['GET'])
# def get(self, book_id):
#     return rate.get_book_rating()
#
#
# api.add_resource(Get_Ratings, '/rate/<book_id>')

# --------------------------------
class Library_List(Resource):
    def get(self):
        return library.get_all_library(session['userid'])

    def post(selfs):
        return library.add_book_to_library(request, session['userid'])


api.add_resource(Library_List, '/library')

if __name__ == '__main__':
    app.run(debug=True)
