from models import User
from flask import jsonify

def get_all_library():
    user_logged_in = User.query.get(2)
    booklist = user_logged_in.user_library
    response = []

    for book in booklist:
        response.append({'id': book.id, 'bookName': book.bookName, 'image': book.image, 'description': book.description})

    return jsonify(response)