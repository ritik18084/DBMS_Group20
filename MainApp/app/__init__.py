from flask import Flask
from os import urandom
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="ayan2000",
  database="testDatabase"
)


def create_app():
    app = Flask(__name__)
    app.secret_key = urandom(24)
    
    from .auth import auth
    from .main import main
    from .client import client
    from .agent import agent
    from .staff import staff
    from .admin import admin
    from .shareholders import shareholders
    from .organizations import organizations
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(client)
    app.register_blueprint(agent)
    app.register_blueprint(staff)
    app.register_blueprint(admin)
    app.register_blueprint(shareholders)
    app.register_blueprint(organizations)
    

    # from .admin import viewBranchDetails
    # app.jinja_env.globals.update(viewBranchDetails=viewBranchDetails)

    return app