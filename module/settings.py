from app import mongo
from flask import jsonify
from flask_restful import Resource, reqparse
from datetime import datetime
from bson.objectid import ObjectId

parser = reqparse.RequestParser()


class Settings(Resource):

    def get(self):
        try:
            records = mongo.db.settings.find({})
            output = [record for record in records]
            
            return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': output[0]})

        except Exception as e:
            print('\033[31m' + 'Exception in GET function of Settings class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})


    def put(self):
        parser.add_argument('id', type=str)
        parser.add_argument('threshold', type=int)
        args = parser.parse_args()

        try:
            if args['id'] and args['threshold']:
                mongo.db.settings.update_one(
                    {"_id": ObjectId(args['id'])},
                    {'$set': {'threshold': args['threshold'], 'last_updated': datetime.now().utcnow()}}
                    )
                
                return jsonify({'message': 'Records updated successfully!', 'error': False, 'data': None})
            else:
                return jsonify({'message': 'Missing field \'threshold\'', 'error': True, 'data': None})

        except Exception as e:
            print('\033[31m' + 'Exception in POST function of Settings class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while updating records', 'error': True, 'data': None})
