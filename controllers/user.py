import datetime
import string

import requests
from flask import jsonify, g, render_template, session
from flask_api import FlaskAPI
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm

from models import User

# app and db initiation
app = FlaskAPI(__name__, instance_relative_config=True)
db = SQLAlchemy()
auth = HTTPBasicAuth()


# Users Login
def get_auth_token(request):
    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password(request.json['password']):
        headers = {
            "Description": "Invalid username/password supplied",
        }
        response = jsonify("Invalid username/password supplied")
        response.status_code = 400
        response.headers = headers
        return response

    auth_token = user.encode_auth_token(user.id, user.username)
    if auth_token:
        headers = {
            "Description": "OK",
            "X-Expires-After": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5)
        }
        token = {
            'token': str(auth_token)
        }
        response = jsonify(token)
        response.status_code = 200
        response.headers = headers

        return response


# Get User Profile
def get_user(username):
    alphabet = set(string.ascii_lowercase)
    allowed = ['_', alphabet]
    user = User.query.filter_by(username=username).first()
    if username not in allowed:
        headers = {
            "Description": "Invalid username supplied",
        }

        response = jsonify("Invalid username supplied")
        response.status_code = 403
        response.headers = headers

        return response
    elif user is None:
        headers = {
            "Description": "User not found",
        }

        response = jsonify("User not found")
        response.status_code = 404
        response.headers = headers

        return response
    else:
        user = {"username": user.username,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                # "balance": user.balance,
                "phone": user.phone}
        headers = {
            "Description": "successful operation",
        }

        response = jsonify(user)
        response.status_code = 200
        response.headers = headers

        return response


# Return List of Users
def users_list():
    userlist = User.get_all()
    results = []

    for userslist in userlist:
        obj = {
            "id": userslist.id,
            "username": userslist.username,
            "firstname": userslist.firstname,
            "lastname": userslist.lastname,
            "email": userslist.email,
            "password": userslist.password_hash,
            "balance": userslist.balance,
            "phone": userslist.phone
        }
        results.append(obj)
    response = jsonify(results)
    response.status_code = 200
    return response


# User Create User
def create_user(request):
    alphabet = set(string.ascii_lowercase)
    allowed = ['_', alphabet]
    if request.json['password'] != request.json['password2']:
        headers = {
            "Description": "Invalid Input"
        }
        invalid = {
            "invalid_fields": [
                {
                    "field": "password2",
                    "reason": "Your password did not matched!"
                }
            ]
        }
        response = jsonify(invalid)
        response.status_code = 400
        response.headers = headers
        return response
    elif request.json['username'] not in allowed or request.json['username'][0] not in alphabet:
        headers = {
            "Description": "Invalid Input"
        }
        invalid = {
            "invalid_fields": [
                {
                    "field": "username",
                    "reason": "Should only contain lowercase and should start with a letter"
                }
            ]
        }
        response = jsonify(invalid)
        response.status_code = 400
        response.headers = headers
        return response
    elif request.json['balance'] in alphabet:
        headers = {
            "Description": "Invalid Input"
        }
        invalid = {
            "invalid_fields": [
                {
                    "field": "balance",
                    "reason": "Should only contain numbers"
                }
            ]
        }
        response = jsonify(invalid)
        response.status_code = 400
        response.headers = headers
        return response
    else:
        users = User(
            username=request.json['username'],
            lastname=request.json['lastname'],
            firstname=request.json['firstname'],
            email=request.json['email'],
            password_hash=request.json['password'],
            phone=request.json['phone'],
            role=request.json['role'],
            balance=request.json['balance']
        )

        users.set_password(request.json['password'])

        headers = {
            "Description": "OK"
        }

        User.save(users)
        response = jsonify(users.user_obj())
        response.status_code = 200
        response.headers = headers
        return response


# User Logout
def log_out():

    headers = {
        "Description": "OK",
    }
    response = jsonify("OK")
    response.status_code = 200
    response.headers = headers
    return response
