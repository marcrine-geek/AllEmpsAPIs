from flask import Flask
from db import db
from config import DevelopmentConfig
from flask_cors import CORS 

from backend.models import UserModel

from flask_restx import Resource, abort
from flask import request
import jwt
import re
import datetime
import functools
from werkzeug.security import generate_password_hash, check_password_hash
import config
from time import gmtime, strftime
from db import db
from flask import current_app as app
import json

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

CORS(app)


@app.route('/', methods=['GET'])
def hello():
    return "hello"

def login_required(method):
    @functools.wraps(method)
    def wrapper(self):
        header = request.headers.get('Authorization')
        _, token = header.split()
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except jwt.DecodeError:
            return {'message':'Token is not valid.', 'status':400}
        except jwt.ExpiredSignatureError:
            return {'message':'Token is expired.', 'status': 400}
        email = decoded['email']
        if len(UserModel.query.filter_by(email = email).all()) == 0:
            return {'message':'User is not found.', 'status':400}
        user = UserModel.query.filter_by(email = email).all()[0]
        return method(self, user)
    return wrapper

#Register route
@app.route('/signup', methods =['POST'])
@login_required
def signup():
    email = request.json['email']
    password = request.json['password']
    user = UserModel.query.filter_by(email = email).all()
    if user.email == 0:
        if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email):
            return {'message':'email is not valid.','status':400}
        if len(password) < 6:
            return {'message':'password is too short.','status':400}

        if len(UserModel.query.filter_by(email = email).all()) != 0:
            return {'message':'email is already used.', 'status':400}
        else:
            user = UserModel(email= email, password =generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

        return {'email': email,'mesage':'user registered successfully','status':201}
    else:
        return {"message":"Unauthorized user", "status":400}

#login route
@app.route('/login', methods =['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    
    if len(UserModel.query.filter_by(email = email).all()) == 0:
        return {'message':'User is not found.','status':400}
    user = UserModel.query.filter_by(email = email).all()[0]
    if user.email == 1:
        if not check_password_hash(user.password, password):
            return {'message':'Password is incorrect.', 'status':400}

        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])
        encoded = jwt.encode({'email': email,'userid':user.id, 'exp': exp}, app.config['SECRET_KEY'], algorithm='HS256')

        return { 'message':'successful login', 'email': email, 'token': encoded.decode('utf-8'),'status':200}
    else:
        return {"message":"Unauthorized user", "status":400}

if __name__ == '__main__':    
    app.run()
