import os

import requests
from flask import request, session, redirect, flash, url_for, render_template, make_response, jsonify, \
    send_from_directory
from flask_login import LoginManager, logout_user, login_user
from app import app
from forms import RegistrationForm, LoginForm
from services.controllers import Users_Controller as uc, \
    Genre_Controller as gc, Books_Controller as bc
from models import User

# Authentication
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, decode_token, jwt_required, set_access_cookies, unset_jwt_cookies
)
from blacklist_helpers import is_token_revoked

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chardeanheinrichdanzel')

# Login
login = LoginManager(app)
login.login_view = 'login'

# ------------- Authentication  Setup--------
jwt = JWTManager(app)

# setup
ACCESS_EXPIRES = timedelta(minutes=15)
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['JWT_SECRET_KEY'] = 'TeamLing96'


# Define our callback function to check if a token has been revoked or not
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@jwt.expired_token_loader
@jwt.invalid_token_loader
@jwt.revoked_token_loader
@jwt.user_loader_error_loader
@jwt.unauthorized_loader
def my_expired_token_callback(response):
    print response
    return jsonify({
        "message": "Authentication information is missing or invalid"
    }), 401


@app.route('/')
def landing():
    if 'token' in session:
        token = session['token']
        return render_template('landing/landing.html', token=token)
    else:
        return render_template('landing/landing.html', token=None)


@app.route('/index', methods=['GET'])
def index():
    if 'token' in session:
        # return render_template('index.html', title='Dashboard')
        resp = make_response(render_template('index.html'))
        resp.set_cookie('userID', session['token'])
        return render_template('index.html', title='Dashboard')

    else:
        return redirect('/login')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'token' in session:
        return render_template('admin/index.html', title='Home', user='Hi Admin!', page='Dashboard')
    else:
        return redirect('/login')


@app.route('/ad-dashboard', methods=['GET'])
def ad_dashboard():
    return send_from_directory("templates", "admin/dashboard.html")


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == "GET":
        if 'token' not in session:
            return uc.login()
        else:
            return redirect('/index')
    else:
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


@app.route('/logout')
def out():
    session.pop('token', None)
    session.clear()
    requests.post('http://localhost:5000/users/logout')
    return redirect('/login')


@app.route('/ulist', methods=['GET'])
def users_list():
    if 'token' in session:
        return uc.users_list()
    else:
        return redirect('/login')


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


@app.route('/validate', methods=['POST'])
def validate():
    return uc.validate(requests)


# Books
@app.route('/genres', methods=['GET'])
def genre():
    if 'token' in session:
        return gc.genre()
    else:
        return redirect('/login')


@app.route('/addgenre', methods=['GET'])
def addgenre():
    if request.method == 'GET':
        return send_from_directory("templates", "admin/add_genre_form.html")


@app.route('/deletegenre/<id>', methods=['POST'])
def deletegenre(id):
    return gc.deletegenre(id)


@app.route('/add-book', methods=['GET'])
def books_view():
    return send_from_directory("templates", "admin/add_book_form.html")
    # return render_template('books/book_list2.html')


@app.route('/admin-books', methods=['GET'])
def admin_books():
    return send_from_directory("templates", "admin/booklist.html")
    # return render_template('books/book_list2.html')


@app.route('/books', methods=['GET', 'POST'])
def books():
    # if 'token' in session:
    if request.method == 'GET':
        return bc.books()
    else:
        return bc.post_books(requests)


@app.route('/deletebook/<id>', methods=['POST'])
def deletebook(id):
    return bc.deletebook(id)


@app.route('/users', methods=['GET'])
def users():
    if 'token' in session:
        return uc.users()
    else:
        return redirect('/login')


@app.route('/view-genre', methods=['GET'])
def view_genre():
    return send_from_directory("templates", "admin/view_genre_form.html")


@app.route('/view-book', methods=['GET'])
def view_book():
    return send_from_directory("templates", "admin/view_book_form.html")


@app.route('/view-user', methods=['GET'])
def view_user():
    return send_from_directory("templates", "admin/view_users_form.html")


@app.route('/my_library', methods=['GET'])
def library():
    return render_template('my_library.html')


@app.route('/book-genre', methods=['GET'])
def book_gen():
    return send_from_directory("templates", "admin/edit_book_form.html")


@app.route('/bg/<id>', methods=['GET'])
def bg(id):
    return gc.bg_query(id)


@app.route('/editbook', methods=['POST'])
def edit_book():
    gc.book_genre(request)
    return send_from_directory("templates", "admin/view_book_form.html")


@app.route('/update_genre', methods=['POST'])
def edit_gen():
    gc.edit_genre(request)
    return send_from_directory("templates", "admin/view_genre_form.html")


@app.route('/editgenre', methods=['GET'])
def show_gen_form():
    return send_from_directory("templates", "admin/edit_genre_form.html")


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=80)
