# Initialization of admin blueprint
from flask import Flask
from .views import auth, home, admin

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(admin)


