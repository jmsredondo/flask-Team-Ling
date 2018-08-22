from flask import jsonify
from models import Genre
from models import Book


def genrelist():
    # GET
    genreQuery = Genre.get_all()
    genreList = []

    if genreQuery:
        for genreItem in genreQuery:
            obj = {'id': genreItem.id, 'type': genreItem.type, 'genre': genreItem.genre}
            genreList.append(obj)
        headers = {
            "Description": "OK"
        }
        response = jsonify(genreList)
        response.status_code = 200
        response.headers = headers
        return response


def add_new_genre(request):
    # if request.is_json:
    #     converted_request = request.get_json()
    #     if "type" in converted_request.keys() and "genre" in converted_request.keys():
    #
    #     else:
    #         return jsonify({'message': 'Invalid Request'})
    # else:
    #     return jsonify({'message': 'Invalid Request'})

    type = request.json['type']
    genre = request.json['genre']

    if type is not None:
        new_genre = Genre(type=type, genre=genre)
        Genre.save(new_genre)
        headers = {
            "Description": "OK"
        }
        result = {'id': new_genre.id, 'type': new_genre.type, 'genre': new_genre.genre}
        response = jsonify(result)
        response.status_code = 200
        response.headers = headers
        return response
    else:
        headers = {
            "Description": "Invalid input"
        }
        result = {
            "invalid_fields": [
                {
                    "field": "type",
                    "reason": "Type field is required"
                }
            ]
        }
        response = jsonify(result)
        response.status_code = 400
        response.headers = headers
        return response


def get_genre(id):
    genreQuery = Genre.query.filter_by(id=id).first()
    if genreQuery is not None:
        result = {'id': genreQuery.id, 'type': genreQuery.type, 'genre': genreQuery.genre}
        headers = {
            "Description": "OK"
        }
        response = jsonify(result)
        response.status_code = 200
        response.headers = headers
        return response
    else:
        headers = {
            "Description": "Genre not found"
        }
        response = jsonify("Genre not found")
        response.status_code = 404
        response.headers = headers
        return response


def add_book_genre(request, id):
    genre_object = Genre().query.get(id)
    book = Book.book_info(request.json['book_id'])
    if genre_object and book:
        book.genres.append(genre_object)
        Genre.save(book)
        headers = {
            "Description": "OK"
        }
        result = {"genre_id": genre_object.id, "book_id": book.id}
        response = jsonify(result)
        response.status_code = 200
        response.headers = headers
        return response
    elif book is None:
        headers = {
            "Description": "Invalid Input"
        }
        result = {
            "invalid_fields": [
                {
                    "field": "book_id",
                    "reason": "Book id does not exist"
                }
            ]
        }
        response = jsonify(result)
        response.status_code = 400
        response.headers = headers
        return response


def delete_genre(id):
    genre_object = Genre().query.get(id)
    if genre_object is not None:
        obj = {'id': genre_object.id, 'type': genre_object.type, 'genre': genre_object.genre}
        headers = {
            "Description": "OK"
        }
        Genre.delete(genre_object)
        response = jsonify(obj)
        response.status_code = 200
        response.headers = headers
        return response
    else:
        headers = {
            "Description": "Category not found"
        }
        response = jsonify("Category not found")
        response.status_code = 404
        response.headers = headers
        return response
