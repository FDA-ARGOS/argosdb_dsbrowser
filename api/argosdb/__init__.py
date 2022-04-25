import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from flask_restx import Api, Resource, fields

from .dataset import api as dataset_api
from .organism import api as organism_api
from .biosample import api as biosample_api
from .assembly import api as assembly_api
from .ngsfile import api as ngsfile_api
from .siteann import api as siteann_api
from .records import api as records_api




def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    
    api = Api(app, version='1.0', title='ArgosDB APIs', description='Documentation for the ArgosDB APIs',)
    api.add_namespace(dataset_api)
    api.add_namespace(organism_api)
    api.add_namespace(biosample_api)
    api.add_namespace(assembly_api)
    api.add_namespace(ngsfile_api)
    api.add_namespace(siteann_api)
    api.add_namespace(records_api)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if app.config["ENV"] == "production":
        app.config.from_pyfile('config.prd.py', silent=True)
    else:
        app.config.from_pyfile('config.dev.py', silent=True)

    jwt = JWTManager(app)



    from . import db

    from . import misc
    app.register_blueprint(misc.bp)

    #from . import auth
    #app.register_blueprint(auth.bp)

    #from . import pdataset
    #app.register_blueprint(pdataset.bp)



    app.add_url_rule('/', endpoint='index')



    return app
