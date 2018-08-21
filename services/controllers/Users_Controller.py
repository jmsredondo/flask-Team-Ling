import requests
from flask import render_template, redirect, url_for, flash, request, session, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, logout_user, login_user, LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from app import app
from forms import *

auth = HTTPBasicAuth()
db = SQLAlchemy()

# Login
login = LoginManager(app)
login.login_view = 'login'


# Users Index
def user_index():
    return render_template('index.html', title='Home', user='Hi user!', page='Dashboard')


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
        'password_hash': form.password.data,
        'phone': form.phone.data,
        'role': 'user'
    }
    requests.post('http://localhost:5000/users', json=json)
    return redirect('/login')


def new():
    form = RegistrationForm()
    return render_template('newregister.html', title='new register', form=form)


# Logout User
@app.route('/users/logout')
def user_logout():
    logout_user()
    return redirect('/login')


# User Login
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

# User Login
def post_login():
    form = LoginForm()
    try:
        # fetch the user data
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')

        json_user = {
            'username': user.username
        }
        info = requests.post('http://localhost:5000/users/login', json=json_user)
        session['token'] = info.text
        return redirect('/index')
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500


def users():
    return render_template('users.html', title='List of Users')
