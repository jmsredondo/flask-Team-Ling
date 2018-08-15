from flask import jsonify

from app import db
from app.models import Genre, Book


#GET or POST /genre
def genre(request):
    if request.method == 'GET':
        return jsonify(Genre().list_all_genre())
    else:
        if request.is_json:
            converted_request = request.get_json()
            if "type" in converted_request.keys() and "genre" in converted_request.keys():
                type = converted_request['type']
                genre = converted_request['genre']

                new_genre = Genre(type=type, genre=genre)
                db.session.add(new_genre)
                db.session.commit()
                return jsonify({'id': new_genre.id, 'type': new_genre.type, 'genre': new_genre.genre})
            else:
                return jsonify({'message': 'Invalid Request'})
        else:
            return jsonify({'message': 'Invalid Request'})


# GET or DELETE /genre/<genre_id>
def search_or_delete(request, genre_id):
    if request.method == 'GET':
        if Genre().get_genre_by_id(genre_id):
            return jsonify(Genre().get_genre_by_id(genre_id))
        else:
            return jsonify({'message': 'Cannot Find Specified Genre'})
    else:
        genre_object = Genre().query.get(genre_id)
        if genre_object is not None:
            response = {'id': genre_object.id, 'type': genre_object.type, 'genre': genre_object.genre}
            db.session.delete(genre_object)
            db.session.commit()
            return jsonify(response)
        else:
            return jsonify({'message': 'Cannot Find Specified Genre'})

def add_book_to_genre(genre_id,request):
    converted_requested = request.get_json()
    if request.is_json:
        genre_object = Genre().query.get(genre_id)
        if genre_object is not None:
            if "book_id" in converted_requested.keys():
                book = Book().query.get(converted_requested['book_id'])
                if genre_object and book:
                    book.genres.append(genre_object)
                    db.session.add(book)
                    db.commit()
                    return jsonify({"genre_id": genre_object.id, "book_id": book.id})
                else:
                    return jsonify({'message': 'Cannot find Specified book or genre'})
            else:
                return jsonify({'message': 'Invalid Request'})
        else:
            return jsonify({'message':'Not Found'})
    else:
        return jsonify({'message': 'Invalid Request'})