from models import User, Book, db, Rate
from flask import jsonify, session

# sample 1
# get bookid on request??


def get_book_rate_and_comment(userid,bookid,request):
    user_logged_in = User.query.get(userid)
    book = Book.get(bookid)

    if not Book.query.filter_by(id=bookid):
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
    elif request.json['comment'] is None:
        headers = {
            "Description": "Invalid Input"
        }
        result = {
            "invalid_fields": [
                {
                    "field": "comment",
                    "reason": "No Comment was sent"
                }
            ]
        }
        response = jsonify(result)
        response.status_code = 400
        response.headers = headers
        return response
    elif user_logged_in is None:
        headers = {
            "Description": "Authentication error"
        }
        result = {
            "message": "Authentication information is missing or invalid"
        }
        response = jsonify(result)
        response.status_code = 401
        response.headers = headers
        return response
    else:
        rate = Rate(comment=request.json['comment'],
                    rate=request.json['rating'],
                    user_id=user_logged_in,
                    book_id=book)
        Rate.save(rate)
        r = Rate.query.filter_by(user_id=user_logged_in,
                                 book_id=book)
        results = {'book_id': r.user_id,
                   'rate': r.rate,
                   'comment': r.comment,
                   'id': r.id}
        response = jsonify(results)
        response.status_code = 200
        return jsonify(response)


def get_all_book_ratings(bookid):
    bookQuery = Book.query.filter_by(id=bookid).first()
    rateQuery = Rate.query.filter_by(book_id=bookQuery.id)

    result = []
    for rate in rateQuery:
        obj = {
            'book_id': rate.id,
            'rate': rate.rate,
            'comment': rate.comment
        }
        result.append(obj)

    headers = {
        "Description": "OK"
    }

    response = jsonify(result)
    response.status_code = 200
    response.headers = headers
    return response
