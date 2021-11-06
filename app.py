from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_pymongo import PyMongo

from flask.json import JSONEncoder
from bson import json_util

from dotenv import load_dotenv
from pathlib import Path
import os
env_path = Path('.') / 'config/.env'
load_dotenv(dotenv_path=env_path)

import pickle
file_name = "xgb_reg.pkl"
xgb_model = pickle.load(open('./model/'+file_name, "rb"))

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): 
        return json_util.default(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)
api = Api(app)
CORS(app)

from module.data_store import BulkImport
from module.device import Device, DeviceReading, DeviceList
from module.dashboard_stats import DashboardStats

# utils.load_dataset()

@app.route('/')
def root():
    return 'API is up and running...!'


# api.add_resource(BulkImport, '/import-data')
api.add_resource(Device, '/device')
api.add_resource(DashboardStats, '/dashboard-stats')
api.add_resource(DeviceReading, '/device/reading')
api.add_resource(DeviceList, '/list/device')

if __name__ == '__main__':
    app.run(use_reloader=True)

