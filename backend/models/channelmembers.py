from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class CmembersModel(BaseClass, db.Model):
    __tablename__ = "channel_members"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    member = db.Column(db.Boolean, default=False, nullable=False)
