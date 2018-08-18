from flask import jsonify, g, render_template
from flask_api import FlaskAPI
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from app.models import User

# app and db initiation
app = FlaskAPI(__name__, instance_relative_config=True)
db = SQLAlchemy()
auth = HTTPBasicAuth()


# Users Login
def get_auth_token():
    token = g.user.generate_auth_token()
    token = {'token': token.decode('ascii')}

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
    userslist = User.get_all()
    results = []

    for userslist in userslist:
        obj = {
            'id': userslist.id,
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
def create_user(form):
    # if form.validate_on_submit():
    user = User(username=form.username.data,
                lastname=form.lastname.data,
                firstname=form.firstname.data,
                email=form.email.data,
                password_hash=form.password.data,
                phone=form.phone.data,
                role='user'
                )

    user.set_password(form.password.data)

    User.save(user)
    response = jsonify(user)
    response.status_code = 200

    return response



