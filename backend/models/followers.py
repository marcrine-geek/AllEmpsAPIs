# from db import db
# from .helpers import BaseClass
# from sqlalchemy.orm import relationship
# from datetime import datetime

# class FollowersModel(BaseClass, db.Model):
#     __tablename__ = "followers"

#     id = db.Column(db.Integer, primary_key=True)
#     follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     followed_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     following = db.Column(db.Boolean, default=False, nullable=False)
