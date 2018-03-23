# These are the blueprints initialization of authenticated users
from flask import Blueprint
from . import views

auth = Blueprint('auth', __name__)
