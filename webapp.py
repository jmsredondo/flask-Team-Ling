import os

import requests
from flask import request, session, redirect, url_for
from flask_login import LoginManager

from app import app
from services.controllers import Users_Controller as uc,\
    Genre_Controller as gc,Books_Controller as bc

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Login
login = LoginManager(app)
login.login_view = 'login'


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == "GET":
        return uc.login()
    else:
        info = requests.get('http://localhost:5000/users/login')
        if info.status_code == 200:
            session['token'] = info
            return redirect(url_for('index'))


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

@app.route('/genres', methods=['GET'])
def genre():
    return gc.genre()

@app.route('/books', methods=['GET'])
def books():
    return bc.books()

@app.route('/users', methods=['GET'])
def users():
    return uc.users()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
