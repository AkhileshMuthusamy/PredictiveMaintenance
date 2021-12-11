from app import mongo
from flask import jsonify
from flask_restful import Resource, reqparse
from scipy.ndimage import gaussian_filter1d

parser = reqparse.RequestParser()


class SmoothPredictionGraph(Resource):

    def get(self):
        parser.add_argument('id', type=int)
        args = parser.parse_args()

        try:
            if args['id']:
                records = mongo.db.sensor_values.find({'id': args['id']}).sort("_id", 1)
                output = [record['rul'] for record in records]
                smoothed_output = gaussian_filter1d(output, sigma=5)
                return jsonify({'message': 'Records fetched successfully!', 'error': False, 'data': {'rul': output, 'smoothRul': list(smoothed_output)}})
            else:
                return jsonify({'message': 'Missing field \'id\'', 'error': True, 'data': None})

        except Exception as e:
            print('\033[31m' + 'Exception in GET function of SmoothPredictionGraph class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while fetching records', 'error': True, 'data': None})
