from flask import Flask
import requests

from app import app
from services.controllers import Users_Controller as uc


@app.route('/register', methods=['GET', 'POST'])
def register(username):
    return uc.register_form()


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=80)

