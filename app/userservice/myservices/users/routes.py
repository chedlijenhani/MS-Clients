from flask import request, jsonify, Blueprint, current_app, url_for, make_response
from flask_marshmallow import Marshmallow
from userservice.myservices.users.models  import User
from userservice.myservices.groups.models import Group
from userservice import db, bcrypt, login_manager, app
from flask_login import login_user, current_user, logout_user, login_required
from userservice.myservices.users.utils import save_picture
from userservice.myservices.decorators import require_appkey, token_required
from userservice.myservices.device.models import Device
import jwt
from datetime import datetime,timedelta
import werkzeug
import os
users = Blueprint('users', __name__)
# Init marshmallow
@app.before_first_request
def create_tables():
    db.create_all()
ma = Marshmallow(users)
# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id','firstname', 'lastname', 'email', 'phone_number', 'image_profile', 'password', 'dateOfBirth', 'role','governorate','isLogged', 'isCreated','city','street','zipcode')

# Init schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

# Log In
# Input : object json contain the email and password of user
@users.route("/user/login", methods=['GET', 'POST'])
#@require_appkey
def login():
    email = request.json['email']
    pwd = request.json['password']
    user = User.query.filter_by (email=email).first()
    if not user:
        return jsonify({ 'isLogged': False,
                         'msg': "User not registred !"})

    if bcrypt.check_password_hash(user.password, pwd):
        token = jwt.encode (
            { 'id': user.id, 'exp': datetime.utcnow () + timedelta (seconds=1800) },
            current_app.config['SECRET_KEY'])
        user.isLogged =True

        return jsonify ({ 'token': token.decode ('UTF-8'),
                          'idUser': user.id,
                          'isLogged': user.isLogged,
                          'firstname': user.firstname,
                          'lastname': user.lastname,
                          'email': user.email,
                          'dateOfBirth': user.dateOfBirth,
                          'phone_number': user.phone_number,
                          'governorate': user.governorate,
                          'city': user.city,
                          'street': user.street,
                          'zipcode': user.zipcode,
                          'msg': 'User successfully logged in !'
                          })

    user.isLogged = False
    return jsonify ({
        'isLogged': user.isLogged,
        'msg': 'Password incorrect !'
    })


# Logout
@users.route("/user/logout", methods=['GET', 'POST'])
@require_appkey
@token_required
def logout(current_user):
    import datetime
    if not current_user:
        return jsonify ({ 'msg': 'Cannot perform that function, token is missing!' })
    user = User.query.filter_by (email=current_user.email).first ()
    if user is None:
        user.isLogged = True
        return jsonify ({
        'isLogged': user.isLogged,
        'msg': 'Failed to log out !'
    })
    else:
        user.isLogged = False
        db.session.commit()
        current_user = None
        logout_user()
        token = request.headers['x-access-token']
        yesterday = datetime.datetime.now() + datetime.timedelta(days=-1)
        token = None
        return jsonify ({
                'isLogged': user.isLogged,
                'msg': 'User successfully logged out !'
            })
