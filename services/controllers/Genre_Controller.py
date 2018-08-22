from flask import render_template, redirect, url_for, flash, request
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, logout_user, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from forms import *

def genre():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('genre.html', title='Genre')

def addgenre():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # return render_template('book_view.html', title='Genre')

def deletegenre(id):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # return render_template('book_view.html', title='Genre')

