from flask import Flask
from flask_pymongo import PyMongo

# from config import DevelopmentConfig # Import the configuration class
from .main.routes import main
from .api.routes import api
from .extensions import mongo
from dotenv import load_dotenv
from flask_cors import CORS

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

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")

    # if not mongo_uri:
    #     raise RuntimeError("MONGO_URI is not set in the environment variables")

    # app.config["MONGO_URI"] = mongo_uri
    # mongo.init_app(app)

    # app.register_blueprint(main)
    # app.register_blueprint(api, url_prefix='/api')

    return app
