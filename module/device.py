from flask import jsonify
from flask_restful import Resource, reqparse

from app import mongo

from module import utils


parser = reqparse.RequestParser()

MAINTENANCE_THRESHOLD = 50


class Device(Resource):


    def get(self):
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        try:
            if args['id']:
                records = mongo.db.devices.find({'deviceId': args['id']})
                output = [record for record in records]
                return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': output})
            else:
                return jsonify({'message': 'Missing field \'id\'', 'error': True, 'data': None})

        except Exception as e:
            print('\033[31m' + 'Exception in GET function of Device class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})

    def post(self):
        parser.add_argument('device_name', type=str)
        args = parser.parse_args()

        try:
            if args['device_name']:
                mongo.db.devices.insert_one({'name': args['device_name'], 'rul': None, 'cycle_ran': 0, 'status': 0})
                return jsonify({'message': 'Device added successfully!', 'error': False, 'data': None})
            else:
                return jsonify({'message': 'Missing field \'device_name\'', 'error': True, 'data': None})
        except Exception as e:
            print('\033[31m' + 'Exception in POST function of Device class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while storing records', 'error': True, 'data': None})

    def put(self):
        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)
        args = parser.parse_args()

        try:
            if args['id'] and args['name']:
                mongo.db.devices.update_one({'deviceId': args['id']}, {'$set': {'name': args['name']}})
                return jsonify({'message': 'Device updated successfully!', 'error': False, 'data': None})
            else:
                return jsonify({'message': 'Missing field \'id\' or \'name\'', 'error': True, 'data': None})
        except Exception as e:
            print('\033[31m' + 'Exception in PUT function of Device class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while storing records', 'error': True, 'data': None})



    def delete(self):
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        try:
            if args['id']:
                mongo.db.devices.delete_one({'deviceId': args['id']})
                mongo.db.sensor_values.delete_many({'id': args['id']})
                return jsonify({'message': 'Device deleted successfully!', 'error': False, 'data': None})
            else:
                return jsonify({'message': 'Missing field \'id\' or \'name\'', 'error': True, 'data': None})
        except Exception as e:
            print('\033[31m' + 'Exception in DELETE function of Device class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while deleting records', 'error': True, 'data': None})


class DeviceReading(Resource):


    def get(self):
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        try:
            if args['id']:
                records = mongo.db.sensor_values.find({'id': args['id']})
                output = [record for record in records]
                return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': output})
            else:
                return jsonify({'message': 'Missing field \'id\'', 'error': True, 'data': None})

        except Exception as e:
            print('\033[31m' + 'Exception in get function of DeviceInfo class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})


    def post(self):
        parser.add_argument('id', type=int)
        for i in range(1, 22):
            parser.add_argument('sn_'+ str(i), type=float)
        for i in range(1, 4):
            parser.add_argument('cond_'+ str(i), type=float)
        args = parser.parse_args()

        try:
            if args['id']:
                rul = utils.predict_rul(args)
                sensor_readings = dict(args)
                sensor_readings['rul'] = round(float(rul))
                need_maintenance = 1 if sensor_readings['rul'] < MAINTENANCE_THRESHOLD else 0
                mongo.db.devices.update_one({'deviceId': args['id']}, {'$set': {'rul': sensor_readings['rul'], 'status': need_maintenance}})
                mongo.db.sensor_values.insert_one(sensor_readings)
                return jsonify({'message': 'Sensor values stored successfully!', 'error': False, 'data': None})
            else:
                return jsonify({'message': 'Missing field \'id\'', 'error': True, 'data': None})
        except Exception as e:
            print('\033[31m' + 'Exception in POST function of DeviceReading class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while storing records', 'error': True, 'data': None})


class DeviceList(Resource):
    
    def get(self):

        try:
            records = mongo.db.devices.find()
            output = [record for record in records]
            return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': output})
        except Exception as e:
            print('\033[31m' + 'Exception in get function of DeviceList class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})