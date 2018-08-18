from flask import jsonify
from app.models import Genre
from app.models import Book


def genrelist():
    # GET
    genreQuery = Genre.get_all()
    genreList = []
    for genreItem in genreQuery:
        obj = {'id': genreItem.id, 'type': genreItem.type, 'genre': genreItem.genre}
        genreList.append(obj)
    response = jsonify(genreList)
    response.status_code = 200
    return response


def add_new_genre(request):
    if request.is_json:
        converted_request = request.get_json()
        if "type" in converted_request.keys() and "genre" in converted_request.keys():
            type = converted_request['type']
            genre = converted_request['genre']

            new_genre = Genre(type=type, genre=genre)
            Genre.save(new_genre)
            response = jsonify({'id': new_genre.id, 'type': new_genre.type, 'genre': new_genre.genre})
            response.status_code = 200
            return response
        else:
            return jsonify({'message': 'Invalid Request'})
    else:
        return jsonify({'message': 'Invalid Request'})


def get_genre(id):
    genreQuery = Genre.query.filter_by(id=id).first()
    if genreQuery is not None:
        result = {'id': genreQuery.id, 'type': genreQuery.type, 'genre': genreQuery.genre}
        response = jsonify(result)
        response.status_code = 200
        return response


def add_book_genre(request, id):
    converted_requested = request.get_json()
    if request.is_json:
        genre_object = Genre().query.get(id)
        if genre_object is not None:
            if "book_id" in converted_requested.keys():
                book = Book.book_info(converted_requested['book_id'])
                if genre_object and book:
                    book.genres.append(genre_object)
                    Genre.save(book)
                    return jsonify({"genre_id": genre_object.id, "book_id": book.id})
                else:
                    return jsonify({'message': 'Cannot find Specified book or genre'})
            else:
                return jsonify({'message': 'Invalid Request'})
        else:
            return jsonify({'message': 'Not Found'})
    else:
        return jsonify({'message': 'Invalid Request'})


def delete_genre(id):
    genre_object = Genre().query.get(id)
    if genre_object is not None:
        obj = {'id': genre_object.id, 'type': genre_object.type, 'genre': genre_object.genre}
        Genre.delete(genre_object)
        response = jsonify(obj)
        response.status_code = 200
        return response
    else:
        return jsonify({'message': 'Cannot Find Specified Genre'})