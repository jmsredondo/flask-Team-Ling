from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth

from Controllers import Genre_Controller as genre_cont
from app import app
from app.models import Genre

auth = HTTPBasicAuth()


# Genre - Add Or show all
@app.route("/genre", methods=['GET', 'POST'])
def genre():
    if request.method == 'GET':
        return jsonify(Genre().list_all_genre())
    else:
        if request.is_json:
            return jsonify(genre_cont.create_genre(request.get_json()))
        else:
            return jsonify({'message': 'Invalid Request'})


# Delete Or retrieve
@app.route("/genre/<genre_id>", methods=['GET', 'DELETE'])
def search_genre_by_id(genre_id):
    if request.method == 'GET':
        if Genre().get_genre_by_id(genre_id):
            return jsonify(Genre().get_genre_by_id(genre_id))
        else:
            return jsonify({'message': 'Cannot Find Specified Genre'})
    else:
        return jsonify(genre_cont.delete_genre(genre_id))



