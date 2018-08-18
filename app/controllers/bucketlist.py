from flask import request, jsonify
from app.models import Bucketlist


def bucketlists():
    if request.method == "POST":
        name = str(request.data.get('name', ''))
        if name:
            bucketlist = Bucketlist(name=name)
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 201
            return response
    else:
        # GET
        bucketlists = Bucketlist.get_all()
        results = []

        for bucketlist in bucketlists:
            obj = {
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response