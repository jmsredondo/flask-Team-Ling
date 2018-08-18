from flask import render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, logout_user, LoginManager
from flask_sqlalchemy import SQLAlchemy
from app import app
from services.forms import *

auth = HTTPBasicAuth()
db = SQLAlchemy()

# Login
login = LoginManager(app)
login.login_view = 'login'


# Users Index
@app.route('/')
@app.route('/index')
@auth.login_required
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user, page='Dashboard')


@app.route('/register', methods=['GET'])
# Register User
def register_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    return render_template('registration.html', title='Register', form=form)


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

