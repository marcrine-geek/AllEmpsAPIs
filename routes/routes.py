from tkinter.messagebox import NO
from backend.models import UserModel, channels
from backend.models import UserpostsModel
from backend.models import ChannelsModel
from backend.models import CmembersModel
from flask_restx import Resource, abort
from flask import request
import jwt

import re
import datetime
import functools
from flask import make_response, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash
import config
from time import gmtime, strftime
from db import db
from flask import current_app as app

from utils.dto import UserDto
from utils.dto import AuthDto
import json

api = UserDto.api
user = UserDto.user

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


@api.route('/register')
class Register(Resource):
    
    @api.doc('register a user')
    @api.expect(user, validate=True)
    def post(self):
        email = request.json['email']
        password = request.json['password']
        username = request.json['username']
        firstname = request.json['firstname']
        lastname = request.json['lastname']

        user = UserModel.query.filter_by(email = email).all()
        if not user:
            if not re.match(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', email):
                return {'message':'email is not valid.','status':400}
            if len(password) < 6:
                return {'message':'password is too short.','status':400}

            if len(UserModel.query.filter_by(email = email).all()) != 0:
                return {'message':'email is already used.', 'status':400}
            else:
                user = UserModel(email= email, password =generate_password_hash(password), username=username, firstname=firstname, lastname=lastname)
                db.session.add(user)
                db.session.commit()

                channel = 'General'
                members = CmembersModel(user_id = user.id, channel_name = channel)

                db.session.add(members)
                db.session.commit()

            return {'email': email,'message':'user registered successfully','status':200}
        else:
            return {"message":"User already exists", "status":400}


api2 = AuthDto.api
auth = AuthDto.auth

@api.route('/login')
class Login(Resource):
    @api.doc('Login a user')
    @api.expect(auth, validate=True)
    def post(self):
        email = request.json['email']
        password = request.json['password']
        
        user = UserModel.query.filter_by(email = email).first()
        print("this is user", user)
        if user:
            if not check_password_hash(user.password, password):
                return {'message':'Password is incorrect.', 'status':400}

            exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])
            encoded = jwt.encode({'email': email,'userid':user.id, 'exp': exp}, app.config['SECRET_KEY'], algorithm='HS256')

            return { 'message':'successful login', 'email': email, 'token': encoded,'status':200}
        else:
            return {"message":"Unauthorized user", "status":400}
# get user details and update
@api.route('/user/details')
class UserDetails(Resource):
    @login_required
    def get(self, user):
        user = UserModel.query.filter_by(id=user.id).all()
        print(user)
        if user is None:
            return {"message":"user not authorized"}, 400
        else:
            details=[]
            for i in user:
                x = i.__dict__
                print(x)
                details.append(i.firstname)
                details.append(i.lastname)
                details.append(i.username)
                details.append(i.email)

            return {"message":"user details", "data":details}, 200

# post messages in channels
@api.route('/add/post')
class AddPosts(Resource):
    @login_required
    def post(self, user):
        
        post = request.json['post']
        channel_id = request.json['channel_id']

        record = UserpostsModel(post=post, user_id = user.id, channel_id=channel_id)
        
        db.session.add(record) 
        db.session.commit() 
        
        return {"message":"Message sent successfully"}, 200

#get specific channel's posts
@api.route('/channel/posts')
class ChannelPosts(Resource):
    # @login_required
    def get(self):
        channel_id = request.json['channel_id']
        allposts = UserpostsModel.query.filter_by(channel_id=channel_id).first()
        if allposts is None:
            return {"message":"there are no posts"}, 200
        else:
            posts = db.session.query(UserpostsModel).filter_by(channel_id=channel_id).all()

            if posts is None:
                return {"message":"no posts"}, 200
            else:
                posts_store=[]
                for i in posts:
                    posts_store.append(i.post)

                return {"message": "all posts", "data":posts_store}, 200

#get all user's posts
@api.route('/all/user/posts')
class UserPosts(Resource):
    @login_required
    def get(self, user):
        user_details = UserpostsModel.query.filter_by(user_id=user.id).first()
        if user_details is None:
            return {"message":"please log in"}, 400
        else:
            posts = db.session.query(UserpostsModel).filter_by(user_id=user.id).all()

            if posts is None:
                return {"message":"no posts"}, 200
            else:
                posts_store=[]
                for i in posts:
                    posts_store.append(i.post)

                return {"message": "all posts", "data":posts_store}, 200

# add channels
# admin can add a channel
@api.route('/add/channel')
class Channels(Resource):
    # @login_required
    def post(self):
        channel_name = request.json['channel_name']
        channel = ChannelsModel(channel_name=channel_name)

        db.session.add(channel)
        db.session.commit()

        return {"message":"channel added successfully"}

# get all channels
# logged in users can view all channels
@api.route('/all/channels')
class AllChannels(Resource):
    # @login_required
    def get(self):
        channels = db.session.query(ChannelsModel).all()
        if channels is None:
            return {'message':'No channels'}

        else:
            channel_store =[]
            for i in channels:
                channel_store.append(i.channel_name)
            
            
            return {"message": "channels", "data":channel_store}, 200

# join channel 
@api.route('/join/channel')
class Members(Resource):
    @login_required
    def post(self, user):
        members = CmembersModel(user_id = user.id)

        db.session.add(members)
        db.session.commit()

        return {"message":"member added successfully"}, 200

# get all members in a channel
@api.route('/all/channel/members')
class AllMembers(Resource):
    @login_required
    def get(self, user):
        
        members = db.session.query(CmembersModel).filter_by(user_id=user.id).all()

        if members is None:
            return {"message":"no members"}

        else:
            members_store=[]
            for i in members:
                members_store.append(i.user_id)

            return {"message":"members in the channel", "data":members_store}, 200

# users can follow other users 
@api.route('/follow/user')
class Follow(Resource):
    @login_required
    def post(self, user):
        username = request.json['username']
        followed_user = UserModel.query.filter_by(username=username).first()
        if followed_user is None:
            return {"message":"User not found"}, 400
        user.follow(followed_user)
        db.session.commit()
        return {"message":"followed successfully"}, 200

#unfollow a user
@api.route('/unfollow/user')
class UnFollow(Resource):
    @login_required
    def post(self, user):
        username = request.json['username']
        followed_user = UserModel.query.filter_by(username=username).first()
        if followed_user is None:
            return {"message":"User not found"}, 400
        user.unfollow(followed_user)
        db.session.commit()
        return {"message":"Unfollowed successfully"}, 200
