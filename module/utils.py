from typing import List

import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
from app import mongo, xgb_model


def filter_sensors(sensor_readings):
    valid_sensor_readings = []
    valid_sensors_keys = ['sn_2', 'sn_3', 'sn_4', 'sn_7', 'sn_8', 'sn_9', 'sn_11', 'sn_12', 'sn_13', 'sn_14', 'sn_15', 'sn_17', 'sn_20', 'sn_21']
    sensor_readings = dict(sensor_readings)
    
    for key in valid_sensors_keys:
        valid_sensor_readings.append(sensor_readings[key])

    print(valid_sensor_readings)
    return valid_sensor_readings



def predict_rul(sensor_readings):

    try:
        # predicted_rul = xgb_model.predict(np.array([[643.02, 1585.29, 1398.21, 553.9, 2388.04, 9050.17, 47.2, 521.72, 2388.03, 8125.55, 8.4052, 392.0, 38.86, 23.3735]]))
        predicted_rul = xgb_model.predict(np.array([filter_sensors(sensor_readings)]))
        print(predicted_rul)
        return predicted_rul[0]
    except Exception as e:
        print('\033[31m' + 'Exception in predict_rul function', str(e), sep='\n', end='\033[0m\n')
        return None


def multi_predict_rul(sensor_readings: DataFrame):

    try:
        valid_sensors_keys = ['sn_2', 'sn_3', 'sn_4', 'sn_7', 'sn_8', 'sn_9', 'sn_11', 'sn_12', 'sn_13', 'sn_14', 'sn_15', 'sn_17', 'sn_20', 'sn_21']
        predicted_rul = xgb_model.predict(sensor_readings[valid_sensors_keys])
        print(predicted_rul)
        return predicted_rul
    except Exception as e:
        print('\033[31m' + 'Exception in multi_predict_rul function', str(e), sep='\n', end='\033[0m\n')
        return None



    

