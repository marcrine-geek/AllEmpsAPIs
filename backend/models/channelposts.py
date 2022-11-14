from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class ChannelpostsModel(BaseClass, db.Model):
    __tablename__ = "channel_posts"

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    post = db.Column(db.String(255))

    def __init__(self, post):
        self.post = post
