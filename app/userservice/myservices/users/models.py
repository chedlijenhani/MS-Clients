from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, types
from datetime import datetime
from userservice import db
from werkzeug import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin




# Registred User Class/Model

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tel = db.Column(db.String(20), unique=False, nullable=False)
    city= db.Column(db.String(20), nullable=False)
    password= db.Column(db.String(60), nullable=False)
    cin = db.Column(db.Integer, nullable=False)
    address=db.Column(db.String(150), nullable=False)
    isLogged = db.Column(db.Boolean,unique=False, default=False)
    isCreated = db.Column(db.Boolean,unique=False, default=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    # Init constructorlevelConfidence_user,
    def __init__(self, firstname, lastname, email,tel, password, city, cin, address, isLogged, isCreated):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.tel = tel
        self.city = city
        self.password = password
        self.cin = cin
        self.address = address
        self.governorate = governorate
        self.isLogged = False
        self.isCreated = True
        
