from flask import redirect, url_for, send_from_directory, jsonify
from flask_login import current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

from models import Book, db, Book_Category, Genre


def genre():
    # return render_template('admin/genrelist.html', title='Genre')
    return send_from_directory("templates", "admin/genrelist.html")


def deletegenre(id):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # return render_template('book_view.html', title='Genre')


def book_genre(request):
    for i in request.json["genre"]:
        if Book_Category.query.filter_by(genre_id=i).first():
            pass
        else:
            bg = Book_Category(
                book_id=request.json['bid'],
                genre_id=i
            )
            db.session.add(bg)
            db.session.commit()

    # update row to database
    row = Book.query.filter_by(id=request.json['bid']).first()
    row.bookName = request.json['bookname']
    if request.json['image'] is None:
        pass
    else:
        row.image = request.json['image']
    row.description = request.json['description']
    db.session.commit()


def bg_query(id):
    gen = Genre.get_all()
    bg = Book_Category.query.filter_by(book_id=id).all()
    res = []
    genre_obj = []

    for i in bg:
        res.append(i.__dict__)

    for i in res:
        i.pop('_sa_instance_state')
        i.pop('book_id')

    for i in res:
        genre = Genre.query.filter_by(id=i["genre_id"]).first()
        obj = {
            "genre_id": genre.id,
            "genre_desc": genre.genre
        }
        genre_obj.append(obj)

    result = jsonify(genre_obj)
    result.status_code = 200
    return result
