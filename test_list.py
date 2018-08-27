# test_bucketlist.py
import unittest
import os
import json

import requests
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import app_config
from models import User


class UserTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy()
    db.init_app(app)

    def setUp(self):
        """Define test variables and initialize app."""
        self.host = 'http://localhost:5000'
        self.sampleuser = {'username': 'jamjam', 'firstname': 'Jamsell', 'lastname': 'Fama', 'role': 'user',
                           'phone': '09163053885', 'password': 'N0virus02', 'password2': 'N0virus02',
                           'email': 'jamfama18@gmail.com','balance':"0"}

        self.loginuser = {'username': 'jamjamn',
                           'password': 'N0virus02'}

        self.invaliduser = {'username': 'jamjam',
                            'password': 'asdasdasd'}
        # # binds the app to the current context
        # with self.app.app_context():
        #     # create all tables
        #     db.create_all()

    def test_create_user(self):
        """Test register user (POST request)"""
        res = requests.post(self.host + '/users', json=self.sampleuser)
        self.assertEqual(res.status_code, 200)
        res = requests.get(self.host + '/users-list')
        self.assertEqual(res.status_code, 200)
        self.assertIn('jamjam', str(res.text))

    def test_users_list(self):
        """Test get user list (GET request)."""
        res = requests.get(self.host + '/users-list')
        self.assertEqual(res.status_code, 200)
        self.assertIn('jamjam', str(res.text))

    def test_get_user(self):
        res = requests.get(self.host + '/users/jamjam')
        self.assertEquals(res.status_code, 200)
    #  EEROR ON LOGOUT
    def test_user_success_logout(self):
        res = requests.post(self.host + '/users/logout')
        self.assertEqual(res.status_code, 200)

    def test_user_success_login(self):
        res = requests.post(self.host + '/login', json=self.loginuser)
        self.assertEqual(res.status_code, 200)

    def test_user_fail_login(self):
        res = requests.post(self.host + '/users/loginapi', json=self.invaliduser)
        self.assertEqual(res.status_code, 400)

    def test_user_fail_get(self):
        res = requests.get(self.host + '/users/random')
        self.assertEqual(res.status_code, 404)
    #   self.assertEqual(res.status_code, 400)


class BooksTestCase(unittest.TestCase):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy()
    db.init_app(app)

    def setUp(self):
        self.host = 'http://localhost:5000'
        self.samplebook = {"bookname": "booktest",
                           "image": "URL to image",
                           "description": "description"}

        self.emptybook = {"bookname": None,
                           "image": None,
                           "description": None}

    def test_add_new_book(self):
        res = requests.post(self.host + '/book', json=self.samplebook)
        self.assertEqual(res.status_code, 200)

    def test_booklist(self):
        res = requests.get(self.host + '/book')
        self.assertEqual(res.status_code, 200)

    def test_success_get_book(self):
        res = requests.get(self.host + '/book/1')
        self.assertEqual(res.status_code, 200)

    def test_delete_book(self):
        res = requests.delete(self.host+'/book/15')
        self.assertEqual(res.status_code, 200)

    def test_fail_get_book(self):
        res = requests.get(self.host+'/book/80')
        self.assertEqual(res.status_code, 404)

    def test_fail_add_new_book(self):
        res = requests.post(self.host + '/book', json=self.emptybook)
        self.assertEqual(res.status_code, 400)

    def test_fail_delete_book(self):
        res = requests.delete(self.host + '/book/70')
        self.assertEqual(res.status_code, 404)



class GenreTestCase(unittest.TestCase):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy()
    db.init_app(app)

    def setUp(self):
        self.host = 'http://localhost:5000'
        self.samplegenre = {"type": "genreType",
                            "genre": "genre"}

        self.samplebookgenre = {"book_id": "1"}

        self.invalidgenre = { "type": None,
                              "genre": None}

    def test_sucess_add_new_genre(self):
        res = requests.post(self.host + '/genre', json=self.samplegenre)
        self.assertEqual(res.status_code, 200)

    def test_sucess_genrelist(self):
        res = res = requests.get(self.host + '/genre')
        self.assertEqual(res.status_code, 200)

    def test_sucess_get_genre(self):
        res = requests.get(self.host + '/genre/21')
        self.assertEqual(res.status_code, 200)

    def test_sucess_delete_genre(self):
        res = requests.delete(self.host + '/genre/21')
        self.assertEqual(res.status_code, 200)

    def test_success_add_book_genre(self):
        res = requests.post(self.host + '/genre/addbook/99', json=self.samplebookgenre)
        self.assertEqual(res.status_code, 200)

    def test_fail_get_genre_404(self):
        res = requests.get(self.host + '/genre/99')
        self.assertEqual(res.status_code, 404)

    def test_fail_delete_genre(self):
        res = requests.get(self.host + '/genre/99')
        self.assertEqual(res.status_code, 404)

    def test_fail_add_genre(self):
        res = requests.post(self.host + '/genre', json=self.invalidgenre)
        self.assertEqual(res.status_code, 400)

class LibraryTestCase(unittest.TestCase):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy()
    db.init_app(app)
    # session needs to be created for library idk how to

    def setUp(self):
        self.host = 'http://localhost:5000'
        self.samplelibrary = {'user_id': '1',
                              'book_id': '1'}
        self.user_id = {'user_id': '2'}

    # not sure
    # def test_success_get_all_library(self):
    #     res = requests.get(self.host + '/library', json=self.user_id)
    #     self.assertEqual(res.status_code, 200)
    #
    # def test_success_add_book_to_library(self):
    #     res = requests.post(self.host + '/library', )


# class AdminTestCase(unittest.TestCase):
#     app = Flask(__name__)
#     api = Api(app)
#     app.config.from_object(app_config['development'])
#     app.config.from_pyfile('config.py')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
#     db = SQLAlchemy()
#     db.init_app(app)
#
#     def setUp(self):
#         self.host = 'http://localhost:5000'
#         self.adminaccount = {'username': 'jsmith',
#                            'password': 'N0virus02'}

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
