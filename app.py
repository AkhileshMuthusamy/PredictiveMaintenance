import pickle

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_restful import Api

from config._global import Config
from module.encoder import CustomJSONEncoder

xgb_model = pickle.load(open(Config.MODEL_FILE, "rb"))

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config["MONGO_URI"] = Config.MONGO_URI
mongo = PyMongo(app)
api = Api(app)
CORS(app)

from module.dashboard_stats import DashboardStats
from module.device import Device, DeviceList, DeviceReading
from module.predict import PredictFromFile
from module.smoothing import SmoothPredictionGraph
from module.settings import Settings


@app.route('/')
def root():
    return 'API is up and running...!'

api.add_resource(Device, '/device')
api.add_resource(DashboardStats, '/dashboard-stats')
api.add_resource(DeviceReading, '/device/reading')
api.add_resource(DeviceList, '/list/device')
api.add_resource(PredictFromFile, '/predict/file')
api.add_resource(SmoothPredictionGraph, '/predict/smooth')
api.add_resource(Settings, '/settings')

if __name__ == '__main__':
    app.run(use_reloader=True)

