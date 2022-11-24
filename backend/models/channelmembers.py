from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class CmembersModel(BaseClass, db.Model):
    __tablename__ = "channel_members"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_firstname = db.Column(db.String(255), db.ForeignKey('users.firstname'), nullable=False)
    user_lastname = db.Column(db.String(255), db.ForeignKey('users.lastname'), nullable=False)
    