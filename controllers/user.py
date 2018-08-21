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
    auth_token = user.encode_auth_token(user.id, user.username)
    if auth_token:
        token = {
            'token': str(auth_token)
        }
        response = jsonify(token)
        response.status_code = 200

        return response


# Get User Profile
def get_user(username):
    user = User.query.filter_by(username=username).first()
    user = {"username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            # "balance": user.balance,
            "phone": user.phone}

    response = jsonify(user)
    response.status_code = 200

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
            # "balance": user.balance,
            "phone": userslist.phone
        }
        results.append(obj)
    response = jsonify(results)
    response.status_code = 200
    return response


# User Create User
def create_user(request):

    if request.json['password'] != request.json['password2']:
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
        return response

    users = User(
        username=request.json['username'],
        lastname=request.json['lastname'],
        firstname=request.json['firstname'],
        email=request.json['email'],
        password_hash=request.json['password'],
        phone=request.json['phone'],
        role=request.json['role']
    )

    users.set_password(request.json['password_hash'])

    User.save(users)
    response = jsonify(users.user_obj())
    response.status_code = 200
    return response
