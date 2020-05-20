from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, types
from datetime import datetime
from userservice import db
from werkzeug import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from userservice.myservices.followers.models import Follow
# Group Model

class Group (UserMixin,db.Model):
    idGroup = db.Column(db.Integer, primary_key=True)
    name_group = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followers = db.relationship('Follow',backref='follower', lazy='dynamic')

    # Init constructor
    def __init__(self, name_group, created_by):
        """

        :rtype: object
        """
        self.name_group = name_group
        self.created_by = created_by
