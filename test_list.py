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
                           'phone': '09163053885', 'password_hash': 'N0virus02', 'password2': 'N0virus02',
                           'email': 'jamfama18@gmail.com'}

        # # binds the app to the current context
        # with self.app.app_context():
        #     # create all tables
        #     db.create_all()

    def test_Register_User(self):
        """Test register user (POST request)"""
        res = requests.post(self.host + '/users', json=self.sampleuser)
        self.assertEqual(res.status_code, 201)
        res = res = requests.get(self.host + '/users-list')
        self.assertEqual(res.status_code, 200)
        self.assertIn('jamjam', str(res.text))

    def test_api_Get_User_List(self):
        """Test get user list (GET request)."""
        res = res = requests.get(self.host + '/users-list')
        self.assertEqual(res.status_code, 200)
        self.assertIn('jamjam', str(res.text))


    # def test_api_can_get_bucketlist_by_id(self):
    #     """Test ebook_api can get a single bucketlist by using it's id."""
    #     rv = self.client().post('/bucketlists/', data=self.bucketlist)
    #     self.assertEqual(rv.status_code, 201)
    #     result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
    #     result = self.client().get(
    #         '/bucketlists/{}'.format(result_in_json['id']))
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn('Go to Borabora', str(result.data))
    #
    # def test_bucketlist_can_be_edited(self):
    #     """Test ebook_api can edit an existing bucketlist. (PUT request)"""
    #     rv = self.client().post(
    #         '/bucketlists/',
    #         data={'name': 'Eat, pray and love'})
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.client().put(
    #         '/bucketlists/1',
    #         data={
    #             "name": "Dont just eat, but also pray and love :-)"
    #         })
    #     self.assertEqual(rv.status_code, 200)
    #     results = self.client().get('/bucketlists/1')
    #     self.assertIn('Dont just eat', str(results.data))
    #
    # def test_bucketlist_deletion(self):
    #     """Test ebook_api can delete an existing bucketlist. (DELETE request)."""
    #     rv = self.client().post(
    #         '/bucketlists/',
    #         data={'name': 'Eat, pray and love'})
    #     self.assertEqual(rv.status_code, 201)
    #     res = self.client().delete('/bucketlists/1')
    #     self.assertEqual(res.status_code, 200)
    #     # Test to see if it exists, should return a 404
    #     result = self.client().get('/bucketlists/1')
    #     self.assertEqual(result.status_code, 404)
    #
    # def tearDown(self):
    #     """teardown all initialized variables."""
    #     with self.app.app_context():
    #         # drop all tables
    #         db.session.remove()
    #         db.drop_all()
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
#
# class GenreTestCase(unittest.TestCase):
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
#         self.samplebook = {'bookName':'booktest',
#                            'image':'URL\URL to image',
#                            'description': 'description'}
#
#     def test_Add_Book(self):
#         res = requests.post(self.host + '/book', data=self.samplebook)
#         self.assertEqual(res.status_code, 201)
#
#     def test_Book_List(self):
#         res = res = requests.get(self.host+'/book')
#         self.assertEqual(res.status_code, 200)
#
#     def test_Get_Book(self):
#         res = requests.get(self.host+'/book/11')
#         self.assertEquals(res.status_code, 200)
#
#
#     def test_remove_Book(self):
#         res = requests.delete(self.host+'/book/11')
#         self.assertEquals(res.status_code, 200)
#


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
