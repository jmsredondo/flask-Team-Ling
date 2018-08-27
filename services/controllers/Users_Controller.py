import json
from flask_jwt_extended import get_jwt_identity

import requests
from flask import render_template, redirect, url_for, request, session, make_response, jsonify, \
    send_from_directory
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, logout_user, login_user, LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from app import app
from forms import *

auth = HTTPBasicAuth()
db = SQLAlchemy()

# Login
login = LoginManager(app)
login.login_view = 'login'


def account():
    # update row to database
    user = User.query.filter_by(id=get_jwt_identity).first()
    if user.check_password(request.json['oldpassword']):
        user.password = generate_password_hash(request.json['newpassword'])
        db.session.commit()


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

    requests.post('http://localhost:5000/users', json=json)
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
    count = User.query.count()
    obj = {
        "ucount": str(count)
    }
    print(count)
    result = jsonify(obj)
    result.status_code = 200
    return result
