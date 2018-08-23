from models import User, Book, db
from flask import jsonify, session

def get_all_library(userid):
    user_logged_in = User.query.get(userid)
    booklist = user_logged_in.user_library
    response = []

    for book in booklist:
        response.append({'id': book.id, 'bookName': book.bookName, 'image': book.image, 'description': book.description})

    return jsonify(response)

def add_book_to_library(request,userid):
    user_logged_in = User.query.get(userid)
    book_id = request.get_json()
    book_object = Book.query.get(book_id['bookid'])
    if book_object:
        user_logged_in.user_library.append(book_object)
        db.session.add(user_logged_in)
        db.session.commit()
        return jsonify({"genre_name": "gagern", "book_id": book_object.id, "book_name": book_object.bookName})
