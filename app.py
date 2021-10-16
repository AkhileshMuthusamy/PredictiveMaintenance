from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from pathlib import Path
import os
env_path = Path('.') / 'config/.env'
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)
api = Api(app)
CORS(app)

@app.route('/')
def root():
    return 'API is up and running...!'


if __name__ == '__main__':
    app.run(use_reloader=True)

