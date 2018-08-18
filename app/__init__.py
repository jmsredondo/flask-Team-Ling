# app/__init__.py
from flask import request
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from controllers import user, admin, book, comment, genre, library, rate
from app.models import User
from app.forms import RegistrationForm

# local import
from instance.config import app_config

db = SQLAlchemy()


def create_app(config_name):
    from app.models import Bucketlist

    # initialize sql-alchemy
    # db = SQLAlchemy()

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # ----------- User API URI -----------

    # User login
    @app.route('/users/login', methods=['GET', 'POST'])
    def user_login():
        return user.get_auth_token()

    # Get User Profile
    @app.route('/users/<username>', methods=['GET'])
    def get_user(username):
        return user.get_user(username)

    # Show list of user
    @app.route('/users-list', methods=['GET', 'POST'])
    def get_users_list():
        return user.users_list()


    # Create new User
    @app.route('/users', methods=['POST'])
    def register_user():
        form = RegistrationForm()
        return user.create_user(form)

    # ------------------------------------

    # ----------- Book API URI -----------

    # Get all books
    @app.route('/book', methods=['GET', 'POST'])
    def books():
        if request.method == 'GET':  # Get all books
            return book.booklist()
        else:
            return book.add_new_book(request)

    @app.route('/book/<id>', methods=['GET', 'DELETE'])
    def get_book(id):
        if request.method == 'GET': # Get specific book
            return book.get_book(id)
        else: # Delete genra
            return book.delete_book(id)

    # -------------------------------------

    # ----------- Genra API URI -----------

    @app.route('/genre', methods=['GET', 'POST'])
    def genrelist():
        if request.method == 'GET': # Get list of genra
            return genre.genrelist()
        else: # Add new genra
            return genre.add_new_genre(request)

    @app.route('/genre/<id>', methods=['GET', 'DELETE'])
    def get_genre(id):
        if request.method == 'GET': # Get specific genra
            return genre.get_genre(id)
        else: # Delete genra
            return genre.delete_genre(id)

    # Add book to genra
    @app.route('/genre/addbook/<id>', methods=['POST'])
    def add_book_genre(id):
        return genre.add_book_genre(request, id)

    # ---------------------------------------

    # ----------- Library API URI -----------

    # # User Library
    # @app.route('/library', methods=['GET', 'POST'])
    # def library():
    #     if request.method == 'GET': # Get library
    #         return library.get_library(id)
    #     else: # Add new book to library
    #         return genre.add_book_lib(id)

    # ------------------------------------

    # ----------- Rate API URI -----------

    # # Comment/Rate the book
    # @app.route('/rate', methods=['POST'])
    # def rate():
    #     return rate.rate_book()
    #
    # # Get all ratings on the book
    # @app.route('/rate/<book_id>', methods=['GET'])
    # def add_rate(book_id):
    #     return rate.get_book_rating()

    # --------------------------------

    return app

