import flask
from flask import render_template
from flask_httpauth import HTTPBasicAuth
from app import app
from models import User

auth = HTTPBasicAuth()


# Admin Index
@app.route('/admin-dashboard')
# @login_required
def dashboard():
    return render_template('admin/dashboard.html', title='Dashboard', page='Dashboard')


# Admin view Users List
@app.route("/users-list")
# @login_required
def users_list():
    users = User.query.order_by(User.username).all()
    ul = []
    for u in users:
        ul.append(u.__dict__)

    for i in ul:
        i.pop('_sa_instance_state')
        i.pop('role')
        i.pop('password_hash')

    # session['ulist'] = json.dumps(ul)
    # return Response(json.loads(json.dumps(ul)), content_type="application/json")
    return flask.jsonify({'users': ul})
