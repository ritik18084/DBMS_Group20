from flask import Flask
from os import urandom
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="YOURPASSWORD",
  database="testDatabase"
)


def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)
    
    from .auth import auth
    from .main import main
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    from .admin import viewBranchDetails
    app.jinja_env.globals.update(viewBranchDetails=viewBranchDetails)

    return app