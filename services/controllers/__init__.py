from flask_api import FlaskAPI
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = FlaskAPI(__name__, instance_relative_config=True)
db = SQLAlchemy()

login = LoginManager(app)
login.login_view = 'login'