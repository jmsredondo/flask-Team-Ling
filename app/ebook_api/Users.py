from flask import render_template, redirect, url_for, request, jsonify
from flask_api import FlaskAPI
from flask_httpauth import HTTPBasicAuth
from flask_login import logout_user
from flask_sqlalchemy import SQLAlchemy
from services.forms import *
from services.models import User

# app and db initiation
app = FlaskAPI(__name__, instance_relative_config=True)
db = SQLAlchemy()
auth = HTTPBasicAuth()


# Users Index
@app.route('/')
@app.route('/index')
@auth.login_required
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user, page='Dashboard')


# Get User Profile
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template('error/empty.html', message="User not found"), 404
        # return redirect(404)
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
    # GET
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
def create_user():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = RegistrationForm()
    # if form.validate_on_submit():
    user = User(username=form.username.data,
                lastname=form.lastname.data,
                firstname=form.firstname.data,
                email=form.email.data,
                password_hash=form.password.data,
                phone=form.phone.data,
                role='basic'
                )

    user.set_password(form.password.data)

    User.save(user)
    response = jsonify(user)
    response.status_code = 200

    # flash('Congratulations, you are now a registered user!')
    # return redirect(url_for('login'))

    return response


# Create new User
def register():
    form = RegistrationForm(request.form)

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

    return jsonify(user.user_obj())


# Logout User
@app.route('/users/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @app.route('/admin', methods=['GET', 'POST'])
# @app.route('/users/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#
#         if not next_page or url_parse(next_page).netloc != '':
#             if user.role == "admin":
#                 next_page = url_for('dashboard')
#             else:
#                 next_page = url_for('index')
#         return redirect(next_page)
#         # return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)
