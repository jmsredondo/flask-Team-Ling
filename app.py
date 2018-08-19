# app/__init__.py
from flask import request, Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from config import app_config
from forms import RegistrationForm
from models import Bucketlist
from models import User
from controllers import user, admin, book, genre, library, rate

# # initialize sql-alchemy
db = SQLAlchemy()

app = Flask(__name__)
api = Api(app)
app.config.from_object(app_config['development'])
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



# # ----------- User API URI -----------
# User login
class Login(Resource):
    # @app.route('/users/login', methods=['GET', 'POST'])
    def get(self):
        return user.get_auth_token()


api.add_resource(Login, '/users/login')


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
    # @app.route('/users', methods=['POST'])
    def post(self):
        form = RegistrationForm()
        return user.create_user(form)


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
    # @app.route('/genre', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
