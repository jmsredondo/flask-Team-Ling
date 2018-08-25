# app/models.py
import datetime
import os
import jwt

from flask import Flask
from flask_login import UserMixin, LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager  # class for handling a set of commands
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Login
login = LoginManager(app)
login.login_view = 'login'

library = db.Table('library',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                   db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
                   )

book_category = db.Table('book_category',
                         db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
                         db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
                         )


class User(UserMixin, db.Model):
    """This class represents the users table."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(11), nullable=True)
    role = db.Column(db.String(120), default='user')
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Float, nullable=True, default=0)
    user_id = db.relationship('Rate', backref='user', lazy=True)
    user_library = db.relationship('Book', secondary=library, backref=db.backref('user'))

    # JSON OBJECT
    def user_obj(self):
        user_data = {
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'password': self.password_hash,
            'phone': self.phone,
            'role': self.role
        }

        return user_data

    def __init__(self, username, firstname, lastname, email, phone, role, password_hash):
        """initialize with name."""
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.role = role
        self.password_hash = password_hash

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def find_by_username(username):
        b = User.query.filter_by(username=username).first()

    # Login Functions
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def encode_auth_token(self, user_id, user_name):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
                'name': user_name
            }
            return jwt.encode(
                payload,
                os.getenv('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<Users: {}>".format(self.username)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bookName = db.Column(db.String(120))
    image = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    genres = db.relationship('Genre', secondary=book_category, backref=db.backref('books'))
    library = db.relationship('User', secondary=library, lazy='subquery',
                              backref=db.backref('users', lazy=True))
    book = db.relationship('Rate', backref='book', lazy=True)

    def __init__(self, bookName, image, description):
        """initialize with name."""
        self.bookName = bookName
        self.image = image
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Book.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def book_info(book_id):
        b = Book.query.filter_by(id=book_id).first()
        return {'book_name': b.bookName, 'image': b.image, 'description': b.description}


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(120))
    genre = db.Column(db.String(120))

    @staticmethod
    def get_all():
        return Genre.query.all()

    def list_all_genre(self):
        genreQuery = Genre.query.all()
        genreList = []
        for genreItem in genreQuery:
            genreList.append({'id': genreItem.id, 'type': genreItem.type, 'genre': genreItem.genre})
        return genreList

    def get_genre_by_id(id):
        genreQuery = Genre.query.filter_by(id=id).first()
        if genreQuery is not None:
            return {'id': genreQuery.id, 'type': genreQuery.type, 'genre': genreQuery.genre}
        else:
            return False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(120), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
                        nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)


class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }


if __name__ == '__main__':
    manager.run()
