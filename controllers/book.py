from flask import jsonify
from models import Book
from forms import BookForm
import os

from services.controllers import app


def booklist():
    # GET
    books = Book.get_all()
    results = []

    for b in books:
        obj = {
            'book_name': b.bookName, 'image': b.image, 'description': b.description
        }
        results.append(obj)

    response = jsonify(results)
    response.status_code = 200
    return response


def add_new_book(form):
    b = Book(bookName=form.bookName.data, image=form.image.data, description=form.description.data)
    Book.save(b)
    results = {'book_name': form.bookName.data, 'image': form.image.data, 'description': form.description.data}
    response = jsonify(results)
    response.status_code = 201
    return response


def get_book(id):
    b = Book.query.filter_by(id=id).first()
    book = {'book_name': b.bookName, 'image': b.image, 'description': b.description}
    response = jsonify(book)
    response.status_code = 200
    return response


def delete_book(id):
    b = Book.query.filter_by(id=id).first()
    book = {'book_name': b.bookName, 'image': b.image, 'description': b.description}
    Book.delete(b)
    response = jsonify(book)
    response.status_code = 200
    return response
