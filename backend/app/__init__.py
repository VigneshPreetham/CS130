
from flask import Flask
#from config import DevelopmentConfig # Import the configuration class
from .main.routes import main


def create_app():
    app = Flask(__name__)
   # app.config.from_object(DevelopmentConfig) # Use the config class
    app.register_blueprint(main)

    return app