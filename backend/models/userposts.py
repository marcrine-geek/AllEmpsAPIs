from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class UserpostsModel(BaseClass, db.Model):
    __tablename__ = "user_posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post = db.Column(db.String(255))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, post, channel_id):
        self.post = post
        self.user_id = user_id
        self.channel_id = channel_id
