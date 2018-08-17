# app/__init__.py

from flask_api import FlaskAPI
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import ebook_api

# local import
from instance.config import app_config


db = SQLAlchemy()

# Login
# login = LoginManager(app)
# login.login_view = 'login'


def create_app(config_name):
    from app.models import Bucketlist
    from app.ebook_api import BucketList

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # ----------- EXAMPLE -----------
    @app.route('/bucketlists/<id>', methods=['POST', 'GET'])
    def bucketlists(id):
        return BucketList.bucketlists()
    # --------------------------------

    # Insert SwaggerHub routings below, do like example above (DO NOT DELETE)

    return app
