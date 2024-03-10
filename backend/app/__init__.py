from flask import Flask
from flask_pymongo import PyMongo

# from config import DevelopmentConfig # Import the configuration class
from .extensions import mongo
from dotenv import load_dotenv
from flask_cors import CORS
from .utils.database import MongoDBUserCollection
from .utils.database import MongoDBRecipeCollection
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Api




import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    mongo_uri = os.getenv("MONGO_URI")
    app.config["MONGO_URI"] = mongo_uri
    mongo.init_app(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.mongodb_user = MongoDBUserCollection(mongo)
    app.mongodb_recipe = MongoDBRecipeCollection(mongo)
    from .api.routes import blueprint

    app.register_blueprint(blueprint)

    return app



