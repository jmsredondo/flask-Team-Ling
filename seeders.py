from faker import Faker
from flask import Flask
from flask_restful import Api

from models import User

app = Flask(__name__)
api = Api(app)

fake = Faker()
for _ in range(100):
    User.seed(fake)

if __name__ == '__main__':
    app.run()