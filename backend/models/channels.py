from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

class ChannelsModel(BaseClass, db.Model):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    banner = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(255), nullable=True)

    def __init__(self, channel_name):
        self.channel_name = channel_name
        
