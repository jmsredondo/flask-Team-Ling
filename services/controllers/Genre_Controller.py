from flask import redirect, url_for, send_from_directory, jsonify
from flask_login import current_user
import base64

from models import Book, db, Book_Category, Genre


def genre():
    # return render_template('admin/genrelist.html', title='Genre')
    return send_from_directory("templates", "admin/genrelist.html")


def deletegenre(id):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # return render_template('book_view.html', title='Genre')


def book_genre(request):
    bgc = Book_Category.query.filter_by(book_id=request.json['bid']).all()
    print(bgc)

    if request.json["genre"]:
        if bgc:
            for i in bgc:
                Book_Category.delete(i)

        for j in request.json["genre"]:
            bg = Book_Category(
                book_id=request.json['bid'],
                genre_id=j
            )
            Book_Category.save(bg)

    # update row to database
    row = Book.query.filter_by(id=request.json['bid']).first()
    row.bookName = request.json['bookname']
    if request.json['image'] is None:
        pass
    else:
        img = request.json['image']
        img_data = img[img.index(',') + 1::]
        moveto = "static/admin/images/book-" + request.json['bid'] + ".jpg"

        with open(moveto, "wb") as fh:
            fh.write(img_data.decode('base64'))

        row.image = "/" + moveto

    row.description = request.json['description']
    db.session.commit()


def edit_genre(request):
    # update row to database
    row = Genre.query.filter_by(id=request.json['gid']).first()
    row.type = request.json['type']
    row.genre = request.json['genre']
    db.session.commit()


def bg_query(id):
    bg = Book_Category.query.filter_by(book_id=id).join(Genre)
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

    print(genre_obj)
    result = jsonify(genre_obj)
    result.status_code = 200
    return result
