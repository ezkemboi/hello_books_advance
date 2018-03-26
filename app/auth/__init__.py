# These are the blueprints initialization of authenticated users
from flask import Flask
from .views import auth


app = Flask(__name__)
app.register_blueprint(auth)
