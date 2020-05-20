from flask import request, jsonify, Blueprint, current_app, url_for, make_response
from flask_marshmallow import Marshmallow
from userservice.myservices.device.models  import Device
from userservice import db, bcrypt, login_manager, app
from flask_login import login_user, current_user, logout_user, login_required
from userservice.myservices.decorators import require_appkey, token_required
from userservice.myservices.users.models import User
import jwt
from datetime import datetime

devices = Blueprint('devices', __name__)
# Init marshmallow
ma = Marshmallow(devices)
# User Schema
class DeviceSchema(ma.Schema):
  class Meta:
    fields = ('idDevice', 'code_imei', 'user_id')

# Init schema
device_schema = DeviceSchema(strict=True)
devices_schema = DeviceSchema(many=True, strict=True)


# Create Device
@devices.route('/deviceAdd', methods=['POST'])
def create_Device():
        code_imei = request.json['code_imei']
        device = Device.query.filter_by (code_imei=code_imei).first ()
        if not device:
        	new_device = Device(code_imei)
        	db.session.add(new_device)
        	db.session.commit()
        	#return user_schema.jsonify(new_Device)
        	return jsonify ({
            	'msg': 'New device successfully created !'
        	})
        return jsonify ({ 'msg' : 'found' }) 
    	


#getallDevice
@devices.route('/device', methods=['GET'])
@require_appkey
def get_devices():
    all_devices =Device.query.all()
    result = devices_schema.dump(all_devices)
    return jsonify(result.data)

# Delete Device
@devices.route('/device/delete', methods=['DELETE'])
@require_appkey
def delete_device():
  code_imei = request.json['code_imei']
  device = Device.query.filter_by (code_imei=code_imei).first ()

  if not device:
    return jsonify ({ 'msg': 'No device found!' })

  db.session.delete (device)
  db.session.commit ()

  return jsonify ({ 'msg': 'device successfully deleted!' })


# Attach device to user
@devices.route('/device/attach', methods=['PUT'])
@require_appkey
def attachDeviceToUser():
    code_imei= request.json['code_imei']
    # Fetch device
    device = Device.query.filter_by (code_imei=code_imei).first ()
    if not device:
       return jsonify ({ 'msg': 'No device found!' })
    user_id= request.json['user_id']
    device.user_id = user_id
    db.session.commit()
    return jsonify ({ 'msg': 'Device successfully attached!',
                      'isAttached': True,
                      'user_id' : device.user_id
                       })

# detach device from user
@devices.route('/device/detach', methods=['PUT'])
@require_appkey
def detachDeviceFromUser():
    ode_imei= request.json['code_imei']
    # Fetch device
    device = Device.query.filter_by (code_imei=code_imei).first ()
    if not device:
       return jsonify ({ 'msg': 'No device found!' })
    device.user_id = None
    db.session.commit()
    return jsonify ({ 'msg': 'Device successfully dettached!',
                      'isAttached': False
                       })
