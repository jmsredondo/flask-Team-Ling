import os

import requests
from flask import request, session, redirect, url_for, render_template, make_response, jsonify
from flask_login import LoginManager, logout_user, login_user

from app import app
from forms import RegistrationForm, LoginForm
from services.controllers import Users_Controller as uc, \
    Genre_Controller as gc, Books_Controller as bc
from models import User

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chardeanheinrichdanzel')

# Login
login = LoginManager(app)
login.login_view = 'login'


@app.route('/')
def landing():
    return render_template('landing/landing.html')


@app.route('/index', methods=['GET'])
def index():
    if 'token' in session:
        return render_template('index.html', title='Dashboard')
    else:
        return redirect('/login')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'token' in session:
        return render_template('admin/index.html', title='Home', user='Hi Admin!', page='Dashboard')
    else:
        return redirect('/login')


@app.route('/logout')
def out():

    session.clear()
    requests.post('http://localhost:5000/users/logout')
    return redirect('/login')


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == "GET":
        if 'token' not in session:
            return uc.login()
        else:
            return redirect('/index')
    else:
        return uc.post_login()


@app.route('/ulist', methods=['GET'])
def users_list():
    if 'token' in session:
        return uc.users_list()
    else:
        return redirect('/login')


# session.pop('username', None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return uc.register_form()
    elif request.method == "POST":
        return uc.redirect_login(requests)
    else:
        return "error"


@app.route('/newregister', methods=['GET'])
def reg():
    return uc.register_form()


# Books
@app.route('/genres', methods=['GET'])
def genre():
    if 'token' in session:
        return gc.genre()
    else:
        return redirect('/login')


@app.route('/addgenre', methods=['POST'])
def addgenre():
    return gc.addgenre()


@app.route('/deletegenre/<id>', methods=['POST'])
def deletegenre(id):
    return gc.deletegenre(id)

@app.route('/admin-books', methods=['GET'])
def books_view():
    return render_template('books/book_list2.html')

@app.route('/books', methods=['GET', 'POST'])
def books():
    # if 'token' in session:
        if request.method == 'GET':
            return bc.books()
        else:
            return bc.post_books(requests)
    # else:
    #     return redirect('/login')


@app.route('/deletebook/<id>', methods=['POST'])
def deletebook(id):
    return bc.deletebook(id)


@app.route('/users', methods=['GET'])
def users():
    if 'token' in session:
        return uc.users()
    else:
        return redirect('/login')

@app.route('/my_library', methods=['GET'])
def library():
    return render_template('my_library.html')
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)
