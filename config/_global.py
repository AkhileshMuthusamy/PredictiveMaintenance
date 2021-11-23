import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / 'config/.env'
load_dotenv(dotenv_path=env_path)


class Config:

    FILETYPE = {
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'txt': 'text/plain',
        'csv': 'text/csv',
        'csv-ms': 'application/vnd.ms-excel'
        }
    MODEL_FILE = Path('.') / 'model/xgb_reg.pkl'
    MONGO_URI = os.environ.get('MONGO_URI')