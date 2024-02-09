
from flask import Flask
from flask_pymongo import PyMongo
#from config import DevelopmentConfig # Import the configuration class
from .main.routes import main
from .api.routes import api
from .extensions import mongo
import os


def create_app():
    app = Flask(__name__)
   # app.config.from_object(DevelopmentConfig) # Use the config class
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        raise RuntimeError("MONGO_URI is not set in the environment variables")

    app.config["MONGO_URI"] = mongo_uri
    mongo.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')

    return app


