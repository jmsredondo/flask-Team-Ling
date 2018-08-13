import flask
from flask import render_template, json, Response, session
from flask import Flask, session

from app.models import *


def get_users():  # noqa: E501
    users = User.query.order_by(User.username).all()
    ul = []
    for u in users:
        ul.append(u.__dict__)

    for i in ul:
        i.pop('_sa_instance_state')
        i.pop('role')
        i.pop('password_hash')


    # session['ulist'] = json.dumps(ul)
    # return Response(json.loads(json.dumps(ul)), content_type="application/json")
    return flask.jsonify({'users': ul})
