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
            'id': b.id, 'book_name': b.bookName, 'image': b.image, 'description': b.description
        }
        results.append(obj)

    headers = {
        "Description": "OK",
    }

    response = jsonify(results)
    response.headers = headers
    response.status_code = 200
    return response


def add_new_book(request):
    if request.json['bookname'] is None:
        headers = {
            "Description": "Invalid Input"
        }
        invalid = {
            "invalid_fields": [
                {
                    "field": "BookName",
                    "reason": "Book name field should not be empty"
                }
            ]
        }
        response = jsonify(invalid)
        response.status_code = 400
        response.headers = headers
        return response
    elif request.json['image'] is None:
        headers = {
            "Description": "Invalid Input"
        }
        invalid = {
            "invalid_fields": [
                {
                    "field": "image",
                    "reason": "Image field should not be empty"
                }
            ]
        }
        response = jsonify(invalid)
        response.status_code = 400
        response.headers = headers
        return response
    elif request.json['image'] is None and request.json['bookname'] is None:
        headers = {
            "Description": "Invalid Input"
        }
        invalid = {
            "invalid_fields": [
                {
                    "field": "BookName, image",
                    "reason": "BookName and Image field should not be empty"
                }
            ]
        }
        response = jsonify(invalid)
        response.status_code = 400
        response.headers = headers
        return response
    else:
        b = Book(bookName=request.json['bookname'], image=request.json['image'], description=request.json['description'])
        Book.save(b)
        b = Book.query.filter_by(bookName=request.json['bookname']).first()
        results = {'book_name': b.bookName, 'image': b.image, 'description': b.description, "id": b.id}
        response = jsonify(results)
        response.status_code = 200
        return response


def get_book(id):
    b = Book.query.filter_by(id=id).first()
    if b is None:
        headers = {
            "Description": "Book not found",
        }

        response = jsonify("Book not found")
        response.status_code = 404
        response.headers = headers
        return response

    book = {'book_name': b.bookName, 'image': b.image, 'description': b.description}
    response = jsonify(book)
    response.status_code = 200
    return response


def delete_book(id):
    b = Book.query.filter_by(id=id).first()
    book = {'book_name': b.bookName, 'image': b.image, 'description': b.description}
    headers = {
        "Description": "OK",
    }
    Book.delete(b)
    response = jsonify(book)
    response.status_code = 200
    response.headers = headers
    return response
