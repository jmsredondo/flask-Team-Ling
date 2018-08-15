from flask import render_template, flash, redirect, url_for, request, Response, jsonify
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
    if form.validate():
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
    else:
        return jsonify(form.errors)

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


@app.route('/addbook', methods=['GET'])
def book_form_add():
    form = BookForm()
    return render_template('addbook.html', form=form)


# Get all books
# Add A new book
@app.route("/book", methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        form = BookForm(request.form)
        return jsonify(Book().add(form.bookName.data, form.image.data, form.description.data))
    else:
        # return list of books
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
# Genre - Add Or show all
@app.route("/genre", methods=['GET', 'POST'])
def routeGenre():
    return genre_cont.genre(request)


# Delete Or retrieve
@app.route("/genre/<genre_id>", methods=['GET', 'DELETE'])
def search_genre_by_id(genre_id):

    if request.method == 'GET':
        if Genre().get_genre_by_id(genre_id):
            return jsonify(Genre().get_genre_by_id(genre_id))
        else:
            return jsonify({'message': 'Cannot Find Specified Genre'})
    else:
        return jsonify(genre_cont.delete_genre(genre_id))

    return genre_cont.search_or_delete(request, genre_id)


@app.route("/genre/addbook/<genre_id>", methods=['POST'])
def add_genre_to_routes(genre_id):
    return genre_cont.add_book_to_genre(genre_id,request)




