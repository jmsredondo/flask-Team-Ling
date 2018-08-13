from flask import render_template, flash, redirect, url_for, request
from app import app
from app import db
from app.forms import *
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from Controllers.Admin_Controller import *
from werkzeug.urls import url_parse
from app import models


# Log In User
@app.route('/admin', methods=['GET', 'POST'])
@app.route('/users/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            if user.role == "admin":
                next_page = url_for('dashboard')
            else:
                next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# User Logout
@app.route('/users/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


# Users Index
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user, page='Dashboard')


# Admin Index
@app.route('/admin-dashboard')
@login_required
def dashboard():
    return admin_dashboard()

# Admin Index
@app.route('/users-list')
@login_required
def users_list():
    return admin_dashboard()


# Error Handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500