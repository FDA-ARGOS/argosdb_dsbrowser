import os,sys
import json
import traceback
from flask import (Blueprint,request,jsonify,current_app)
from argosdb.db import get_mongodb, log_error, next_sequence_value
from flask_restx import Resource, Api
bp = Blueprint('misc', __name__, url_prefix='/misc')

#api = Api(current_app)
api = Api(bp)


@bp.route('/hello', methods=('GET', 'POST'))
class HelloWorld(Resource):
    def hello(self):
        return "Hello!"



@bp.route('/hello_world', methods=('GET', 'POST'))
def hello_world():
    res_obj = {
        "message":"Hello World!",
        "instance_path":current_app.instance_path,
        "secret_key":current_app.config["SECRET_KEY"]
    }
    return jsonify(res_obj), 200


@bp.route('/info', methods=('GET', 'POST'))
def info():
    res_obj = {"config":{}}
    #k_list = ["DB_HOST", "DB_NAME", "DB_USERNAME", "DB_PASSWORD",  "DATA_PATH"]
    k_list = ["DB_HOST", "DB_NAME", "DB_USERNAME", "DATA_PATH"]
    for k in k_list:
        res_obj["config"][k] = current_app.config[k]
    mongo_dbh, error_obj = get_mongodb()
    res_obj["connection_status"] = "success" if error_obj == {} else error_obj
    return jsonify(res_obj), 200

@bp.route('/verlist', methods=('GET', 'POST'))
def verlist():

    mongo_dbh, error_obj = get_mongodb()
    if error_obj != {}:
        return jsonify(error_obj), 200
    res_obj = {"verlist":[]}
    for coll in mongo_dbh.collection_names():
        if coll.find("c_bco_v-") != -1:
            rel = coll[8:]
            res_obj["verlist"].append(rel)
    return jsonify(res_obj), 200
    



