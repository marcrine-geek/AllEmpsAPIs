from backend.models import UserModel
from backend.models import UserpostsModel
from backend.models import ChannelsModel
from backend.models import CmembersModel
from flask_restx import Resource, abort
from flask import request, session
from flask_jwt_extended import create_access_token, decode_token
import jwt
from flask import Flask
from flask import current_app as app
from config import DevelopmentConfig
from flask_caching import Cache

import re
import datetime
import functools
from flask import make_response, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash
import config
from time import gmtime, strftime
from db import db
from flask import current_app as app
from services.mail_service import send_email

from utils.dto import UserDto
from utils.dto import AuthDto
import json

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
cache = Cache(app)

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

# forgot password
@api.route('/forgot')
class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'

        body = request.get_json()
        email = body.get('email')
        if not email:
            return {"message": "wrong email"}

        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return {"message": "email does not exist"}

        expires = datetime.timedelta(hours=24)
        reset_token = create_access_token(
            str(user.id), expires_delta=expires)

        return send_email('[Adamur] Reset Your Password',
                          sender='adamurtests@gmail.com',
                          recipients=[user.email],
                          text_body=render_template('email/reset_password.txt',
                                                    url=url + reset_token),
                          html_body=render_template('email/reset_password.html',
                                                    url=url + reset_token))

# reset password
@api.route('/reset')
class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        body = request.get_json()
        reset_token = body.get('reset_token')
        password = body.get('password')

        if not reset_token or not password:
            return {"message": "an error occured"}

        user_id = decode_token(reset_token)['sub']

        print("+++++++++++", user_id)

        user = UserModel.query.filter_by(id=user_id).first()

        if user:
            user.password = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()

            return send_email('[Adamur] Password reset successful',
                              sender='adamurtests@gmail.com',
                              recipients=[user.email],
                              text_body='Password reset was successful',
                              html_body='<p>Password reset was successful</p>')

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
            cols = ['firstname', 'lastname', 'username', 'email']
            
            result = [{col: getattr(d, col) for col in cols} for d in user]
            
            return jsonify(data=result)

# post messages in channels
# completed
@api.route('/add/post')
class AddPosts(Resource):
    @login_required
    def post(self, user):
        
        post = request.json['post']
        channel_id = request.json['channel_id']
        channel_name = request.json['channel_name']

        member = db.session.query(CmembersModel).filter_by(channel_name=channel_name).all()
        if member:

            record = UserpostsModel(post=post, user_id = user.id, channel_id=channel_id)
        
            db.session.add(record) 
            db.session.commit() 
        
            return {"message":"Message sent successfully"}, 200
        
        else:
            return {"message":"Not allowed to send messages to this channel. Join channel first"}, 400

#get specific channel's posts
# complete
@api.route('/channel/posts')
class ChannelPosts(Resource):
    # @login_required
    def get(self):
        channel_id = request.args.get('id')
        channels = ChannelsModel.query.filter_by(id=channel_id).first()
        if channels is None:
            return {"message":"That channel does not exist"}, 400
        else:
            posts = db.session.query(UserpostsModel).filter_by(channel_id=channel_id).all()
            
            if posts is None:
                return {"message":"no posts"}, 200
            else:
                cols = ['user_id', 'post']
            
                result = [{col: getattr(d, col) for col in cols} for d in posts]
            
                return jsonify(data=result)

#get all user's posts
# complete
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
                cols = ['user_id', 'post']
            
                result = [{col: getattr(d, col) for col in cols} for d in posts]
            
                return jsonify(data=result)

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
            cols = ['id', 'channel_name']
            
            result = [{col: getattr(d, col) for col in cols} for d in channels]
            
            return jsonify(data=result)

# join channel 
@api.route('/join/channel')
class Members(Resource):
    @login_required
    def post(self, user):
        channel_name = request.json['channel_name']
        members = CmembersModel(user_id = user.id, channel_name = channel_name)

        db.session.add(members)
        db.session.commit()

        return {"message":"member added successfully"}, 200

# get all members in a channel
@api.route('/all/channel/members')
class AllMembers(Resource):
    @login_required
    def get(self, user):
        #check if channel exists
        channel_name = request.args.get('channel_name')

        members = db.session.query(CmembersModel).filter_by(channel_name=channel_name).all()

        if members:
            
            cols = ['user_id', 'channel_name']
            
            result = [{col: getattr(d, col) for col in cols} for d in members]
            
            return jsonify(data=result)
        
        else:
            return {"message":"channel does not exists"}

# users can follow other users 
# complete
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
# complete
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

# all followers
# complete
@api.route('/all/followers')
class Followers(Resource):
    @login_required
    def get(self, user):
        member = UserModel.query.filter_by(id=user.id).first()
        if member:
            x = user.allfollowers(member)
            db.session.commit()
            
            cols = ['firstname', 'lastname']
        
            result = [{col: getattr(d, col) for col in cols} for d in x]
        
            return jsonify(followers=result)
        
        else:
            return {"message":"user not found"}

# get posts for all followed users by a user
# complete
@api.route('/followed/posts')
class Follow(Resource):
    @login_required
    def get(self, user):
        follower = UserModel.query.filter_by(id=user.id).first()
        if follower is None:
            return {"message":"user not found"}, 400
        
        x = user.followed_posts(follower)
        db.session.commit()

        print(x)
        cols = ['post']
        
        result = [{col: getattr(d, col) for col in cols} for d in x]
    
        return jsonify(posts=result)
        