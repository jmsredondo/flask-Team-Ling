# app/__init__.py
import controllers
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


def service_app(config_name):
    from services.controllers import Users_Controller as uc

    return app
