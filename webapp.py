import os

import requests
from flask import request, session, redirect, flash, url_for, render_template, make_response, jsonify, \
    send_from_directory
from flask_login import LoginManager, logout_user, login_user
from app import app
from forms import RegistrationForm, LoginForm
from services.controllers import Users_Controller as uc, \
    Genre_Controller as gc, Books_Controller as bc
from config import app_config

# Authentication
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, decode_token, jwt_required, set_access_cookies, unset_jwt_cookies,
    get_jwt_claims, get_jwt_identity
)
from blacklist_helpers import is_token_revoked, prune_database

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chardeanheinrichdanzel')
app.config.from_object(app_config['development'])

# Login
login = LoginManager(app)
login.login_view = 'login'

# ------------- Authentication  Setup--------
jwt = JWTManager(app)

# setup
ACCESS_EXPIRES = timedelta(hours=8)
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
def my_expired_token_callback(response=None):
    if 'access_token_cookie' in request.cookies:
        return logout()
    else:
        return uc.login()


#------Admin Routes -------
@app.route('/dashboard', methods=['GET'])
@jwt_required
def dashboard():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return render_template('admin/index.html', title='Home', user='Hi Admin!', page='Dashboard')
    return redirect('/')

@app.route('/ad-dashboard', methods=['GET'])
@jwt_required
def ad_dashboard():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return send_from_directory("templates", "admin/dashboard.html")
    return uc.login()

@app.route('/addgenre', methods=['GET'])
@jwt_required
def addgenre():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            if request.method == 'GET':
                return send_from_directory("templates", "admin/add_genre_form.html")
    return uc.login()


@app.route('/deletegenre/<id>', methods=['POST'])
@jwt_required
def deletegenre(id):
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return gc.deletegenre(id)
    return uc.login()


@app.route('/add-book', methods=['GET'])
@jwt_required
def books_view():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return send_from_directory("templates", "admin/add_book_form.html")
    return uc.login()
    # return render_template('books/book_list2.html')

@app.route('/deletebook/<id>', methods=['POST'])
@jwt_required
def deletebook(id):
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return bc.deletebook(id)
    return uc.login()


@app.route('/users', methods=['GET'])
@jwt_required
def users():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return uc.users()
    return uc.login()


@app.route('/view-genre', methods=['GET'])
@jwt_required
def view_genre():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return send_from_directory("templates", "admin/view_genre_form.html")
    return uc.login()

@app.route('/bg/<id>', methods=['GET'])
@jwt_required
def bg(id):
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return gc.bg_query(id)
    return uc.login()

@app.route('/editbook', methods=['POST'])
@jwt_required
def edit_book():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            gc.book_genre(request)
            return send_from_directory("templates", "admin/view_book_form.html")
    return uc.login()


@app.route('/update_genre', methods=['POST'])
@jwt_required
def edit_gen():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            gc.edit_genre(request)
            return send_from_directory("templates", "admin/view_genre_form.html")
    return uc.login()

@app.route('/editgenre', methods=['GET'])
@jwt_required
def show_gen_form():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return send_from_directory("templates", "admin/edit_genre_form.html")
    return uc.login()


@app.route('/admin-books', methods=['GET'])
@jwt_required
def admin_books():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'admin':
            return send_from_directory("templates", "admin/booklist.html")
    return uc.login()
    # return render_template('books/book_list2.html')

#---------- End of Admin Routes --------


#------- Users Route ------

@app.route('/my_library', methods=['GET'])
@jwt_required
def library():
    claims = get_jwt_claims()
    if claims:
        if claims['role'] == 'user':
            return render_template('my_library.html')
    return uc.login()

#-------------------------



@app.route('/')
def landing():
    prune_database()
    if 'access_token_cookie' in request.cookies:
        decoded_token = decode_token(request.cookies['access_token_cookie'])
        if 'user_claims' in decoded_token:
            claims = decoded_token['user_claims']
            if 'role' in claims:
                if claims['role'] == 'user':
                    token = 'yeah'
                    return render_template('landing/landing.html', token=token)
                elif claims['role'] == 'admin':
                    return redirect('/dashboard')
    return render_template('landing/landing.html', token=None)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == "GET":
        if 'access_token_cookie' in request.cookies:
            token = decode_token(request.cookies['access_token_cookie'])
            if 'identity' in token:
                return redirect('/')
        return uc.login()
    else:
        form = LoginForm()
        # try:
        # fetch the user data
        json_user = {
            'username': form.username.data,
            'password': form.password.data
        }

        resp = requests.post('http://localhost:5000/users/login', json=json_user)
        response_info = resp.json()
        response = make_response(redirect('/'))
        if 'token' in response_info:
            set_access_cookies(response, response_info['token'])
        else:
            flash('Invalid username/password supplied')
            return uc.login()
        return response
        # except:
        #     return 'Invalid username/password supplied'


@app.route('/logout')
@jwt_required
def out():
    try:
        return logout()
    except:
        return redirect('/login')


@app.route('/userslist', methods=['GET'])
# @jwt_required
def users_list():
    # identity = get_jwt_identity()
    # if identity == 'admin':
    return uc.users_list()


# else:
#     return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'access_token_cookie' in request.cookies:
        token = decode_token(request.cookies['access_token_cookie'])
        if 'identity' in token:
            return redirect('/')
    if request.method == "GET":
        return uc.register_form()
    elif request.method == "POST":
        return uc.redirect_login(requests)
    else:
        return "error"

@app.route('/validate', methods=['POST'])
def validate():
    if request.is_json:
        username_in_json = request.get_json()
        if 'username' in username_in_json:
            return uc.validate(username_in_json['username'])
    else:
        return jsonify({'message': False})
# Books

@app.route('/genres', methods=['GET'])
@jwt_required
def genre():
    return gc.genre()


@app.route('/books', methods=['GET', 'POST'])
@jwt_required
def books():
    # if 'token' in session:
    if request.method == 'GET':
        return bc.books()
    else:
        return bc.post_books(requests)

@app.route('/view-book', methods=['GET'])
@jwt_required
def view_book():
    return send_from_directory("templates", "admin/view_book_form.html")

@app.route('/view-user', methods=['GET'])
@jwt_required
def view_user():
    return send_from_directory("templates", "admin/view_users_form.html")

@app.route('/book-genre', methods=['GET'])
@jwt_required
def book_gen():
    return send_from_directory("templates", "admin/edit_book_form.html")

@app.route('/bookgenrelist', methods=['GET'])
def show_bookgenlist():
    return bc.bookgenrelist()


@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        return send_from_directory("templates", "admin/account_form.html")
    else:
        return uc.account(request)


@app.route('/users-count', methods=['GET'])
def users_count():
    return uc.users_count()

def logout():
    to_send_cookies = {
        'access_token_cookie': request.cookies['access_token_cookie']
    }
    # to_send_headers = {
    #     'X-CSRF-TOKEN': request.cookies['csrf_access_token']
    # }

    # response = requests.post('http://localhost:5000/users/logout', cookies=to_send_cookies, headers=to_send_headers)
    requests.post('http://localhost:5000/users/logout', cookies=to_send_cookies)
    response = make_response(redirect('/login'))
    unset_jwt_cookies(response)
    session.clear()
    return response

if __name__ == '__main__':
    app.run(host='', port=9500)
    # app.run(debug=True, port=80)
