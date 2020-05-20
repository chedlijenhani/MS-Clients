from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, types
from datetime import datetime
from userservice import db
from werkzeug import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin



# Follow Model

class Follow(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column (db.Integer, db.ForeignKey ('group.idGroup'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Init constructor
    def __init__(self, follower_id, followed_at,group_follower_id ):
        self.group_id = group_id
        self.user_id = user_id
