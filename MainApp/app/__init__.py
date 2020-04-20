from flask import Flask
from os import urandom
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="YOUR_PASSWORD",
  database="DATABASE_NAME"
)


def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)
    
    from .auth import auth
    from .main import main

    app.register_blueprint(main)
    app.register_blueprint(auth)
    

    return app