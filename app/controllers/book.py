from flask import jsonify
from app.models import Book
from app.forms import BookForm

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


def add_new_book(request):
    form = BookForm(request.form)
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
    b = Book.book_info(id)
    Book.delete(b)
    response = jsonify(b)
    response.status_code = 200
    return response
