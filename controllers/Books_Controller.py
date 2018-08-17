from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth

from app import app
from app.forms import *
from app.models import Book

auth = HTTPBasicAuth()


# Get all books
# Add A new book
@app.route("/book", methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        form = BookForm(request.form)
        b = Book(bookName=form.bookName.data, image=form.image.data, description=form.description.data)
        b.session.add(b)
        b.session.commit()
        return jsonify(
            [{'book_name': form.bookName.data, 'image': form.image.data, 'description': form.description.data}])
    else:
        books = jsonify(Book().book())
        return books


# Get a book object
# Delete a book object
@app.route("/book/<book_id>", methods=['GET', 'DELETE'])
def bookinfo(book_id):
    if request.method == 'DELETE':
        return jsonify(Book().delete(book_id))
    else:
        return jsonify(Book().book_info(book_id))