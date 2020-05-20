from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, types,JSON,Float
from datetime import datetime
from userservice import db
from werkzeug import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin




# Device Model

class Device(UserMixin,db.Model):
    idDevice = db.Column(db.Integer, primary_key=True)
    code_imei=db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Init constructor
    def __init__(self,code_imei):
        self.code_imei=code_imei
