# Initialization of admin blueprint
from flask import Blueprint
from . import views

admin = Blueprint('admin', __name__)

