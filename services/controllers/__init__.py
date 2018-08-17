# app/__init__.py

from flask_api import FlaskAPI
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

app = FlaskAPI(__name__, instance_relative_config=True)
db = SQLAlchemy()

# Login
login = LoginManager(app)
login.login_view = 'login'


def create_app(config_name):

    from app.ebook_api import Users

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # ----------- API URI -----------

    # Get User Profile
    @app.route('/register', methods=['GET', 'POST'])
    def get_user(username):
        return Users.get_user(username)

    # Show list of user
    @app.route('/users-list', methods=['GET', 'POST'])
    def get_users_list():
        return Users.users_list()

    # Create new User
    @app.route('/users', methods=['POST'])
    def register_user():
        return Users.create_user()
    # --------------------------------


    return app




