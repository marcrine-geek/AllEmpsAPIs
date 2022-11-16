from db import db
from .helpers import BaseClass
from sqlalchemy.orm import relationship
from datetime import datetime

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

    def __init__(self, firstname, lastname, username, email, password):
        now = datetime.now()
        self.registered_on = now.strftime("%Y-%m-%d %H:%M:%S")
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
