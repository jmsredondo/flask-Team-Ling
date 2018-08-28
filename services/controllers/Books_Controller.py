from flask import render_template, redirect, url_for, jsonify
from flask_login import current_user

from forms import *
from models import Book, Book_Category, Genre


def bookgenrelist():
    # GET
    books = Book.query.outerjoin(Book_Category, Book.id == Book_Category.book_id).outerjoin(Genre,
                                                                                            Book_Category.genre_id == Genre.id).add_columns(
        Genre.genre, Book.id, Book.bookName, Book.description, Book.image)
    results = []

    for b in books:
        obj = {
            'id': b.id, 'book_name': b.bookName, 'image': b.image, 'description': b.description, 'genre': b.genre
        }
        results.append(obj)

    headers = {
        "Description": "OK",
    }

    response = jsonify(results)
    response.headers = headers
    response.status_code = 200
    return response


def books():
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


    requests.post('/book', json=json)
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

