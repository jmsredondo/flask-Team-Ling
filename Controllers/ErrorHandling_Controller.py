from flask import render_template
from flask_httpauth import HTTPBasicAuth

from app import app
from app import db

auth = HTTPBasicAuth()


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