from app import db
import json
from app.models import Genre

def create_genre(request):
    if "type" in request.keys() and "genre" in request.keys():
        type = request['type']
        genre = request['genre']
        try:
            new_genre = Genre(type=type, genre=genre)
            db.session.add(new_genre)
        except:
            db.session.rollback()
        db.session.commit()
        return {'id':new_genre.id, 'type': new_genre.type, 'genre': new_genre.genre}
    else:
        return {'message':'Invalid Request'}

def delete_genre(id):
    genre = Genre().query.get(id)
    try:
        if genre is not None:
            response = {'id': genre.id, 'type': genre.type, 'genre': genre.genre}
            db.session.delete(genre)
            db.session.commit()
            return response
        else:
            return {'message':'Cannot Find Specified Genre'}
    except:
        db.session.rollback()



