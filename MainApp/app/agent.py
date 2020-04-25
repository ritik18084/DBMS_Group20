from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType

agent = Blueprint('agent',__name__)

@agent.route('/viewsold', methods= ['POST'])
def viewsold():
    if not(userLoggedIn() and userType('agent')):
        return
    dbCursor = db.cursor()
    sql = "SELECT ins_type FROM INSURANCE_DATABASE WHERE agent_ID=%s"
    val = (session['id'],)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return res

@agent.route('/viewagentprofile', methods= ['POST'])
def viewagentprofile():
    if not(userLoggedIn() and userType('agent')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM AGENT_DATABASE WHERE agent_ID=%s"
    val = (session['id'])
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return res

@agent.route('/getClientContact', methods= ['POST'])

def getClientContact():
    if not(userLoggedIn() and userType('agent'))
        return
    dbCursor = db.cursor()
    sql = "SELECT client_name, client_ph, client_email \
    FROM AGENT_DATABASE WHERE agent_ID= %s and client_ID = %s"
    agent_ID = session['id']
    client_ID = session['id']
    val = (agent_ID,client_ID)
    dbCursor.execute(sql, val)
    res= dbCursor.fetchall()
    dbCursor.close()
    return res