from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType

agent = Blueprint('agent',__name__)

@agent.route('/viewsold', methods= ['POST'])
def viewsold():
    if not(userLoggedIn() and userType('agent')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM policy_database WHERE agent_ID=%s"
    val = (session['id'])
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return res

@agent.route('/viewagentprofile', methods= ['POST'])
def viewagentprofile():
    if not(userLoggedIn() and userType('agent')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM agent_database WHERE agent_ID=%s"
    val = (session['id'])
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return res

