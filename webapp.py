import os

from flask import Flask, request
import requests

from app import app
from services.controllers import Users_Controller as uc

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == "GET":
        return uc.login()
    else:
        info = requests.get('http://localhost:5000/users/login')
        return info.text


@app.route('/register', methods=['GET', 'POST'])
def register():
    return uc.register_form()


@app.route('/newregister', methods=['GET'])
def reg():
    return uc.register_form()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

