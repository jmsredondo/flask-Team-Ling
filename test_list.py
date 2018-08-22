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
                           'email': 'jamfama18@gmail.com'}

        # # binds the app to the current context
        # with self.app.app_context():
        #     # create all tables
        #     db.create_all()

    def test_create_user(self):
        """Test register user (POST request)"""
        res = requests.post(self.host + '/users', json=self.sampleuser)
        self.assertEqual(res.status_code, 200)
        res = res = requests.get(self.host + '/users-list')
        self.assertEqual(res.status_code, 200)
        self.assertIn('jamjam', str(res.text))
        user = User.query.filter_by(username='jamjam').first()
        User.delete(user)

    def test_users_list(self):
        """Test get user list (GET request)."""
        res = res = requests.get(self.host + '/users-list')
        self.assertEqual(res.status_code, 200)
        self.assertIn('jamjam', str(res.text))

    def test_get_user(self):
        res = requests.get(self.host + '/users/jsmith')
        self.assertEquals(res.status_code, 200)

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
        self.samplebook = {'bookName': 'booktest',
                           'image': 'URL\URL to image',
                           'description': 'description'}

    def test_add_new_book(self):
        res = requests.post(self.host + '/book', data=self.samplebook)
        self.assertEqual(res.status_code, 201)

    def test_booklist(self):
        res = res = requests.get(self.host+'/book')
        self.assertEqual(res.status_code, 200)

    def get_book(self):
        res = requests.get(self.host+'/book/80')
        self.assertEquals(res.status_code, 200)


    def test_delete_book(self):
        res = requests.delete(self.host+'/book/11')
        self.assertEquals(res.status_code, 200)


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
        self.samplegenre = {'type':'genreType',
                           'genre':'genre'}
        self.samplebookgenre = {'book_id': '1'}

    def test_add_new_genre(self):
        res = requests.post(self.host + '/genre', data=self.samplegenre)
        self.assertEqual(res.status_code, 200)

    def test_genrelist(self):
        res = res = requests.get(self.host+'/genre')
        self.assertEqual(res.status_code, 200)

    def test_get_genre(self):
        res = requests.get(self.host+'/genre/21')
        self.assertEquals(res.status_code, 200)


    def test_delete_genre(self):
        res = requests.delete(self.host+'/genre/21')
        self.assertEquals(res.status_code, 200)

    def add_book_genre(self):
        res = requests.post(self.host + '/genre/addbook/<id>',data=self.samplebookgenre)
        self.assertEquals(res.status_code, 200)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
