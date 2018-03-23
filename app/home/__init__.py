# These are general blueprint for users, guests and homepages.
from flask import Blueprint
from . import views

home = Blueprint('home', __name__)
