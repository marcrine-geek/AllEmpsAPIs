from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class FollowersModel(BaseClass, db.Model):
    __tablename__ = "followers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
