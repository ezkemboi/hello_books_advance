from flask import Flask
from flask_restful import Api
from config import app_config

# Import from models
from app.models import User, Book


app = Flask(__name__)
api = Api(app)

app.config.from_object(app_config['development'])


