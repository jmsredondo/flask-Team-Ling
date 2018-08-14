import json
from flask import render_template, flash, redirect, url_for, request, Response, jsonify, g
from app import app
from app import db
from app.forms import *
from flask_login import current_user, login_user
from app.models import User, Book, Genre
from flask_login import logout_user
from flask_login import login_required
from Controllers import Admin_Controller as ac
from Controllers import Genre_Controller as genre_cont
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()



# Log In User
@app.route('/admin', methods=['GET', 'POST'])
@app.route('/users/login', methods=['GET', 'POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


@app.route('/users/<username>', methods=['GET', 'POST'])
@auth.login_required
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template('error/empty.html', message="User not found"), 404
    return jsonify({"username": user.username})
    #                ,
    # "firstName": user.firstName,
    # "lastName": user.lastName,
    # "email": user.email,
    # "balance": user.balance,
    # "phone": user.phone})


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


# User Logout
@app.route('/users/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# User Register
@app.route('/register', methods=['GET'])
def register_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    # if form.validate_on_submit():
    #
    #     user = User(username=form.username.data,
    #                 lastname=form.lastname.data,
    #                 firstname=form.firstname.data,
    #                 email=form.email.data
    #                 )
    #
    #     user.set_password(form.password.data)
    #
    #     #db.session.add(user)
    #     #db.session.commit()
    #     return jsonify(user.__repr__())
    # flash('Congratulations, you are now a registered user!')
    # return redirect(url_for('login'))

    return render_template('registration.html', title='Register', form=form)


@app.route('/users', methods=['POST'])
def register():
    form = RegistrationForm(request.form)

    user = User(username=form.username.data,
                lastname=form.lastname.data,
                firstname=form.firstname.data,
                email=form.email.data,
                password_hash=form.password.data,
                phone=form.phone.data,
                role='basic'
                )

    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.user_obj())


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
    return render_template('admin/dashboard.html', title='Dashboard', page='Dashboard')


# Admin view Users List
@app.route("/users-list")
# @login_required
def users_list():
    return ac.get_users()
    # return render_template("admin/users.html", title='Users', page='Users List', data=ac.get_users())


# Get all books
# Add A new book
@app.route("/book", methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        form = BookForm(request.form)
        b = Book(bookName = form.bookName.data, image = form.image.data, description = form.description.data)
        b.session.add(b)
        b.session.commit()
        return jsonify([{'book_name': form.bookName.data, 'image':form.image.data, 'description':form.description.data}])
    else:
        books = jsonify(Book().book())
        return books


# Get a book object
# Delete a book object
@app.route("/book/<book_id>", methods=['GET', 'DELETE'])
def bookinfo(book_id):
    if request.method == 'DELETE':
        return jsonify(Book().delete(book_id))
    else:
        return jsonify(Book().book_info(book_id))


#Genre - Add Or show all
@app.route("/genre", methods=['GET', 'POST'])
def genre():
    if request.method == 'GET':
        return jsonify(Genre().list_all_genre())
    else:
        if request.is_json:
            return jsonify(genre_cont.create_genre(request.get_json()))
        else:
            return jsonify({'message':'Invalid Request'})

#Delete Or retrieve
@app.route("/genre/<genre_id>", methods=['GET', 'DELETE'])
def search_genre_by_id(genre_id):
    if request.method == 'GET':
        if Genre().get_genre_by_id(genre_id):
            return jsonify(Genre().get_genre_by_id(genre_id))
        else:
            return jsonify({'message':'Cannot Find Specified Genre'})
    else:
        return jsonify(genre_cont.delete_genre(genre_id))


# Error Handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/empty.html', message="NOT FOUND"), 404


# Error Handling
@app.errorhandler(401)
def authentication_error(error):
    return render_template('error/empty.html', message="NOT AUTHORIZED"),


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()

    return render_template('error/empty.html', message="INTERNAL ERROR"), 500
