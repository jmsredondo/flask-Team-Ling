from flask import render_template
from flask_api import FlaskAPI
from werkzeug.utils import redirect

app = FlaskAPI(__name__, instance_relative_config=True)


@app.route('/hi/', methods=['POST', 'GET'])
def hi():
    return render_template('login.html', title='Sign In')