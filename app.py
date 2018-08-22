# app/__init__.py
import os
from flask import request, Flask, render_template, url_for,session
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from controllers import user, book, genre,library
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

# initialize sql-alchemy
from models import User

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
api = Api(app)
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy()
db.init_app(app)
SESSION_TYPE = 'redis'
app.secret_key = 'teamling'
# ------------- Authentication --------
# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']

# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
app.config['JWT_COOKIE_SECURE'] = False

# Set the cookie paths, so that you are only sending your access token
# cookie to the access endpoints, and only sending your refresh token
# to the refresh endpoint. Technically this is optional, but it is in
# your best interest to not send additional cookies in the request if
# they aren't needed.
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

# Enable csrf double submit protection. See this for a thorough
# explanation: http://www.redotheweb.com/2015/11/09/api-security.html
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = 'TeamLing'  # Change this!

jwt = JWTManager(app)

# # ----------- User API URI -----------

# User login
class Login(Resource):
    # @app.route('/users/login', methods=['GET', 'POST'])
    def post(self):
        #return user.get_auth_token(request)
        session['userid'] = request.get_json()['userid']
        return session['userid']


api.add_resource(Login, '/users/login')


# User login
class Logout(Resource):
    # @app.route('/users/login', methods=['GET', 'POST'])
    def post(self):
        session.clear()
        return "logged out"
        #return user.log_out()


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
# class Comment_Rate_Book(Resource):
# # @app.route('/rate', methods=['POST'])
#     def post(self):
#         return rate.rate_book()
#
#
# api.add_resource(Comment_Rate_Book, '/rate')
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
        return library.add_book_to_library(request,session['userid'])

api.add_resource(Library_List, '/library')

if __name__ == '__main__':
    app.run(debug=True)
