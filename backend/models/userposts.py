from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class UserpostsModel(BaseClass, db.Model):
    __tablename__ = "user_posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post = db.Column(db.String(255))

    def __init__(self, post):
        self.post = post
