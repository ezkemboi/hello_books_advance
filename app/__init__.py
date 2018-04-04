"""
This module initializes the application
"""
from flask_api import FlaskAPI
from config import app_config

from app.models import User, Book


def create_app(config_name):
    """
    This contains all initialization for application to run
    """
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app
