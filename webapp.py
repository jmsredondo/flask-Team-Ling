from flask import Flask
import requests

from app import app
from services.controllers import Users_Controller as uc


@app.route('/register', methods=['GET', 'POST'])
def register(username):
    return uc.register_form()


@app.route('/newregister', methods=['GET'])
def reg():
    return uc.register_form()


if __name__ == '__main__':
   app.run(debug=True)

