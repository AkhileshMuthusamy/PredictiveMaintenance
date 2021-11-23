from bson import json_util
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj): 
        return json_util.default(obj)
