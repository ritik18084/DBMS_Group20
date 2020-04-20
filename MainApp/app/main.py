from flask import Blueprint, session, request, redirect, url_for
from . import db
from .auth import userLoggedIn

main = Blueprint('main',__name__)

@main.route('/')
def index():
    if userLoggedIn():
        return 'LoggedIn MainPage'
    return 'MainPage'
