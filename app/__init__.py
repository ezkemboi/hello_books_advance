from flask_api import FlaskAPI
from config import app_config

# Import from models
from app.models import User, Book
from app.endpoints import UserLogout, UserRegistration, UserLogin, ResetPassword, Book, SingleBook, Users


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(Users)
    app.register_blueprint(UserLogin)
    app.register_blueprint(UserLogout)
    app.register_blueprint(ResetPassword)
    app.register_blueprint(Book)
    app.register_blueprint(SingleBook)
    return app


