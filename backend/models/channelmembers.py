from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class CmembersModel(BaseClass, db.Model):
    __tablename__ = "channel_members"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channel_name = db.Column(db.String(255), db.ForeignKey('channels.channel_name'))
    