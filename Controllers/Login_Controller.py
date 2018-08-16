from flask import jsonify, g, render_template
from flask_httpauth import HTTPBasicAuth

from app import app
from app.models import User

auth = HTTPBasicAuth()


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/users/login', methods=['GET', 'POST'])
@auth.login_required
def get_auth_token():
    if verify_password is False:
        return render_template('error/empty.html', message="Invalid username/password supplied"), 404

    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user or user is None:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
            # return render_template('error/empty.html', message="Invalid username/password supplied"), 404
    g.user = user
    return True


