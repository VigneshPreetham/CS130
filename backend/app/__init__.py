from flask import Flask
from flask_pymongo import PyMongo

# from config import DevelopmentConfig # Import the configuration class
from .api.routes import api
from .extensions import mongo
from dotenv import load_dotenv
from flask_cors import CORS
from .utils.database import MongoDBUserCollection

import os


def create_app():
    app = Flask(__name__)
    CORS(app)

    # app.config.from_object(DevelopmentConfig) # Use the config class
    dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
    print(dotenv_path)
    load_dotenv(dotenv_path=dotenv_path)

    mongo_uri = os.getenv("MONGO_URI")
    app.config["MONGO_URI"] = mongo_uri
    mongo.init_app(app)

    app.mongodb_user = MongoDBUserCollection(mongo)



    app.register_blueprint(api, url_prefix="/api")

  

    return app
