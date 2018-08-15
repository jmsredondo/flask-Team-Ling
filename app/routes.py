from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth

from Controllers import Genre_Controller as genre_cont
from app import app
from app.models import Genre

auth = HTTPBasicAuth()

import json
from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from app import app
from app import db
from app.forms import *
from flask_login import current_user, login_user
from app.models import User, Book, Genre
from flask_login import logout_user
from flask_login import login_required
from Controllers import Admin_Controller as ac
from Controllers import Genre_Controller as genre_cont
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()



# Genre - Add Or show all
@app.route("/genre", methods=['GET', 'POST'])
def routeGenre():
    return genre_cont.genre(request)


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

    return genre_cont.search_or_delete(request, genre_id)

@app.route("/genre/addbook/<genre_id>", methods=['POST'])
def add_genre_to_routes(genre_id):
    return genre_cont.add_book_to_genre(genre_id,request)




