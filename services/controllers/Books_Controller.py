from flask import render_template, redirect, url_for
from flask_login import current_user

from forms import *


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
