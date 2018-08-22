import requests
from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, logout_user, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse

from forms import *


def genre():
    # return render_template('admin/genrelist.html', title='Genre')
    return send_from_directory("templates", "admin/genrelist.html")


def deletegenre(id):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # return render_template('book_view.html', title='Genre')
