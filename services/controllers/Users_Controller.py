import json
from flask_jwt_extended import get_jwt_identity, jwt_required

import requests
from flask import render_template, redirect, url_for, request, session, make_response, jsonify, \
    send_from_directory, flash
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, logout_user, login_user, LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from app import app
from forms import *
from models import Book, Genre,db

auth = HTTPBasicAuth()

# Login
login = LoginManager(app)
login.login_view = 'login'

@jwt_required
def account(request):
    # update row to database
    id = get_jwt_identity()
    user = User.query.filter_by(id=id).first()
    if request.json['newpassword'] == request.json['password2']:
        if user.check_password(request.json['oldpassword']):
            print(user.password_hash)
            user.password_hash = generate_password_hash(request.json['newpassword'])
            print(request.json['newpassword'])
            print(user.password_hash)

            db.session.commit()

            obj = {
                "status": "success",
                "result": "You've successfully changed your password!"
            }
            result = jsonify(obj)
            return result
    else:
        obj = {
            "status": "fail",
            "result": "Change password failed"
        }

        result = jsonify(obj)
        return result


# Register User
def register_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    return render_template('registration.html', title='Register', form=form)


# Redirect to login page
def redirect_login(requests):
    form = RegistrationForm()
    json = {
        'username': form.username.data,
        'lastname': form.lastname.data,
        'firstname': form.firstname.data,
        'email': form.email.data,
        'password': form.password.data,
        'password2': form.password2.data,
        'phone': form.phone.data,
        'role': 'user'
    }

    requests.post('http://localhost:5056/users', json=json)
    return redirect('/login')


def new():
    form = RegistrationForm()
    return render_template('newregister.html', title='new register', form=form)


# User Login
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)


def users_list():
    return send_from_directory("templates", "admin/userslist.html")


def users():
    return render_template('users.html', title='List of Users')


def users_count():
    ucount = User.query.count()
    bcount = Book.query.count()
    gcount = Genre.query.count()
    count = User.query.count()
    obj = {
        "ucount": str(ucount),
        "bcount": str(bcount),
        "gcount": str(gcount)
    }
    result = jsonify(obj)
    result.status_code = 200
    return result

def validate(username):
    resp = requests.get('http://localhost:5056/users/'+username)

    resp_dict = resp.json()
    if 'username' in resp_dict:
        return jsonify({'message': True})
    else:
        return jsonify({'message':False})
