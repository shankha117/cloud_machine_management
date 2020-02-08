from flask import Flask, request, jsonify, make_response
from flask.json import JSONEncoder
from app.rest.api import cloud_manager
from flask_cors import CORS
from bson import json_util, ObjectId
from datetime import datetime
from config.config_loader import load_config
from app.utils.logger import set_up_logging
import json


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)




"""
create flask app for cmm(cloud machine management)
"""


def create_app():
    cmm = Flask(__name__)

    # insert CORS
    CORS(cmm)

    # add db encoder
    cmm.json_encoder = MongoJsonEncoder

    # register api paths through blueprints
    cmm.register_blueprint(cloud_manager)

    # load configs
    load_config(cmm)

    # set debugger mode
    cmm.config['DEBUG'] = json.loads(cmm.config['debugger'].lower())

    # set logging
    set_up_logging(cmm)

    return cmm


api = create_app()
