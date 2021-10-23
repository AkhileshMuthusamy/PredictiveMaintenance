from flask import jsonify
from flask_restful import Resource, reqparse

from app import mongo


parser = reqparse.RequestParser()


class Device(Resource):


    def get(self):
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        try:
            if args['id']:
                records = mongo.db.devices.find({'id': args['id']})
                output = [record for record in records]
                return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': output})
            else:
                return jsonify({'message': 'Missing field \'id\'', 'error': True, 'data': None})

        except Exception as e:
            print('\033[31m' + 'Exception in GET function of Device class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})

    def post(self):
        parser.add_argument('device_name', type=str)
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        try:
            if args['device_name']:
                mongo.db.devices.insert_one({'id': args['id'], 'name': args['device_name']})
                return jsonify({'message': 'Device added successfully!', 'error': False, 'data': None})
            else:
                return jsonify({'message': 'Missing field \'device_name\'', 'error': True, 'data': None})
        except Exception as e:
            print('\033[31m' + 'Exception in POST function of Device class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while storing records', 'error': True, 'data': None})


class DeviceReading(Resource):


    def get(self):
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        try:
            if args['id']:
                records = mongo.db.sensor_readings.find({'engine_no': args['id']})
                output = [record for record in records]
                return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': output})
            else:
                return jsonify({'message': 'Missing field \'id\'', 'error': True, 'data': None})

        except Exception as e:
            print('\033[31m' + 'Exception in get function of DeviceInfo class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})



class DeviceList(Resource):
    
    def get(self):

        try:
            records = mongo.db.devices.find()
            output = [record for record in records]
            return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': output})
        except Exception as e:
            print('\033[31m' + 'Exception in get function of DeviceList class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})