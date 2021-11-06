from flask import jsonify
from flask_restful import Resource, reqparse

from app import mongo



class DashboardStats(Resource):


    def get(self):

        try:
            stats = {}
            total_records = mongo.db.devices.count_documents({})
            good_devices = mongo.db.devices.count_documents({'status': 0})
            need_maintenance = mongo.db.devices.count_documents({'status': 1})
            stats['totalDevices'] = total_records
            stats['goodCondition'] = good_devices
            stats['needMaintenance'] = need_maintenance
            print(stats)
            return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': stats})

        except Exception as e:
            print('\033[31m' + 'Exception in GET function of DashboardStats class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})
