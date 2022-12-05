from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime
from .userposts import UserpostsModel

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class UserModel(BaseClass, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    image = db.Column(db.LargeBinary)
    registered_on = db.Column(db.DateTime, nullable=False)
    followed = db.relationship(
        'UserModel', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __init__(self, firstname, lastname, username, email, password):
        now = datetime.now()
        self.registered_on = now.strftime("%Y-%m-%d %H:%M:%S")
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = UserpostsModel.query.join(
            followers, (followers.c.followed_id == UserpostsModel.user_id)).filter(
                followers.c.follower_id == self.id)
        own = UserpostsModel.query.filter_by(user_id=self.id)
        return followed.union(own)
