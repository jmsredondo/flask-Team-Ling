from flask import render_template, redirect, url_for, flash, request, send_from_directory, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, logout_user, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from forms import *
from models import book_category, Genre


def books():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('book_view.html', title='Books')
    # return render_template('book_view.html', title='Genre')
    # return send_from_directory("templates", "admin/genrelist.html")


def post_books(requests):
    form = BookForm()
    json = {
        'bookname': form.bookName.data,
        'image': form.image.data,
        'description': form.description.data,
    }

    requests.post('http://localhost:5000/book', json=json)
    return redirect('/login')


def new():
    form = RegistrationForm()
    return render_template('newregister.html', title='new register', form=form)


def addbook():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # return render_template('book_view.html', title='Genre')


def deletebook(id):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # return render_template('book_view.html', title='Genre')



