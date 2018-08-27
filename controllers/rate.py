from models import User, Book, db, Rate
from flask import jsonify, session

# sample 1
# get bookid on request??


def rate_and_comment(user_id, book_id, rate, comment=None):

    if not Book.query.get(book_id):
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
    else:
        rate = Rate(comment=comment,
                    rate=rate,
                    user_id=user_id,
                    book_id=book_id)
        Rate.save(rate)

        results = {'book_id': rate.book_id,
                   'rate': rate.rate,
                   'comment': rate.comment,
                   'id': rate.id}
        response = jsonify(results)
        response.status_code = 200
        return response


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
