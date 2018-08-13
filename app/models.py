import os

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


library = db.Table('library',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

book_category = db.Table('book_category',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(11), unique=True, nullable=True)
    role = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))


    #JSON OBJECT
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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def generate_auth_token(self, expiration=600):
        s = Serializer(os.environ.get('SECRET_KEY'), expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(os.environ.get('SECRET_KEY'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Book(db.Model):
    def __init__(self):
        pass

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(120), index=True, unique=True, nullable=True)
    image = db.Column(db.String(120), index=True, unique=True, nullable=True)
    description = db.Column(db.String(120), index=True, unique=True, nullable=True)
    genres = db.relationship('Genre', secondary=book_category, lazy='subquery',
                           backref=db.backref('books', lazy=True))
    library = db.relationship('User', secondary=library, lazy='subquery',
                             backref=db.backref('users', lazy=True))
    def book(self):
        b = Book.query.all()
        item = []
        for x in b:
            item.append({'book_name': x.book_name,'image':x.image,'description':x.description})
        return item
    def book_info(self,book_id):
        b = Book.query.filter_by(id=book_id).first()
        return [{'book_name': b.book_name,'image':b.image,'description':b.description}]
    def add(self, book_name,image,description):
        b = Book(book_name,image,description)
        b.session.add(b)
        b.session.commit()
        return [{'book_name':book_name,'image':image,'description':description}]
    def delete(self,book_id):
        b = Book.query.filter_by(id=book_id)
        data = b.first()
        delete = b.delete()
        b.session.add(delete)
        b.session.commit()
        return

class Genre(db.Model):
    def __init__(self):
        pass

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(120), index=True, unique=True, nullable=True)
    genre = db.Column(db.String(120), index=True, unique=True, nullable=True)


