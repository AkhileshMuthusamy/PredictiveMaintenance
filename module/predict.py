import numpy as np
import pandas as pd
from app import mongo
from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from module import utils
from config._global import Config

MAINTENANCE_THRESHOLD = 50

parser = reqparse.RequestParser()



class PredictFromFile(Resource):

    def post(self):
        parser.add_argument('id', type=int)
        parser.add_argument('file', type=FileStorage, location='files')
        args = parser.parse_args()

        try:
            if args['id'] and args['file']:

                if args['file'].mimetype == Config.FILETYPE['xlsx']:
                    df = pd.read_excel(args['file'].stream.read())
                    rul = utils.multi_predict_rul(df)
                    df['rul'] = np.round_(rul).astype(int)
                    df.loc[(df['rul'] < 0), ('rul')] = 0
                    df['id'] = args['id']
                    valid_columns = ['id', 'cond_1', 'cond_2', 'cond_3', 'sn_1', 'sn_2', 'sn_3', 'sn_4', 
                                     'sn_5', 'sn_6', 'sn_7', 'sn_8', 'sn_9', 'sn_10', 'sn_11', 'sn_12', 
                                     'sn_13', 'sn_14', 'sn_15', 'sn_16', 'sn_17', 'sn_18', 'sn_19', 'sn_20', 'sn_21', 'rul']
                    # print(list(df[valid_columns].T.to_dict().values()))
                    # print(df.iloc[-1:,:]['rul'].values[0])
                    current_rul = df.iloc[-1:,:]['rul'].values[0]
                    need_maintenance = 1 if current_rul < MAINTENANCE_THRESHOLD else 0
                    print(current_rul, need_maintenance)
                    mongo.db.devices.update_one({'deviceId': args['id']}, {'$set': {'rul': int(current_rul), 'status': need_maintenance}})
                    mongo.db.sensor_values.insert_many(list(df[valid_columns].T.to_dict().values()))
                else:
                    return jsonify({'message': 'Invalid file type', 'error': True, 'data': None})

                return jsonify({'message': 'Sensor values stored successfully!', 'error': False, 'data': None})
            else:
                return jsonify({'message': 'Missing field \'id\' or \'file\'', 'error': True, 'data': None})
        except Exception as e:
            print('\033[31m' + 'Exception in post function of PredictFromExcel class', str(e), sep='\n', end='\033[0m\n')
            return jsonify({'message': 'Error while predicting', 'error': True, 'data': str(e)})
