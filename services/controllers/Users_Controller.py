import requests
from flask import render_template, redirect, url_for, flash, request, session, make_response, jsonify, \
    send_from_directory
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

# User Login
def post_login():
    form = LoginForm()
    try:
        # fetch the user data
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username/password supplied'), 400
            return redirect('/login')

        json_user = {
            'username': user.username,
            'password': user.password_hash
        }

        info = requests.post('http://localhost:5000/users/login', json=json_user)
        session['token'] = info.text
        session['userid'] = user.id
        if user.role == "admin":
            return redirect('/dashboard')
        else:
            return redirect('/')
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500


def users_list():
    # requests.get('http://localhost:5000/users-list')
    # return render_template('admin/userslist.html', title='List of Users')
    return send_from_directory("templates", "admin/userslist.html")


def users():
    return render_template('users.html', title='List of Users')
