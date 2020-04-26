from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from . import db
from random import randint
from datetime import datetime, date
import time
auth = Blueprint('auth',__name__)


def generateUID(length=12):
    uid = str(int(time.time()))
    while len(uid) < length:
        uid = uid + str(randint(0,9))
    return uid

@auth.route('/login')
def loginPage():
    if userLoggedIn():
        return redirect(url_for('shareholders.dashboard'))
    return render_template('login.html')

@auth.route('/signup')
def signupPage():
    if userLoggedIn():
        return redirect(url_for('main.index'))
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    session.pop('loggedIn', None)
    return redirect(url_for('auth.loginPage'))

@auth.route('/login', methods= ['POST'])
def login():
    if userLoggedIn():
        return redirect(url_for('main.index'))
    if validLogin(request.form['email'], request.form['password']):
        loginUser(request.form['email'])
        return redirect(url_for('main.index'))
    flash('Invalid Login Credentials')
    return redirect(url_for('auth.loginPage'))

@auth.route('/signup', methods= ['POST'])
def signup():
    if userLoggedIn():
        return redirect(url_for('main.index'))
    if validateSignupRequest(request.form):
        if userExists(request.form):
            return redirect(url_for('auth.loginPage'))
        addUser(request.form, tp="client")
        loginUser(request.form['email'])
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.signupPage'))        


def addClient(requestForm):
    dbCursor = db.cursor()
    agentID = getAgentID()
    sql = "INSERT INTO client_database VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, %s)"
    val = (requestForm['name'], requestForm['phone'], 
    requestForm['email'], requestForm['aadhar'],
    requestForm['pan'], generateUID(12),
    getAgentID(),
    requestForm['dob'], getAge(requestForm['dob']),
    getGender(requestForm['sex']), "I", requestForm['branch'])
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()

def getAgentID():
    dbCursor = db.cursor(buffered=True)
    sql = "SELECT agent_ID, COUNT(agent_ID) FROM client_database GROUP BY agent_ID ORDER BY COUNT(agent_ID) ASC"
    dbCursor.execute(sql)
    agentID = dbCursor.fetchall()[0][0]
    dbCursor.close()
    return agentID

def getAge(dob):
    dob = datetime.strptime(dob, "%Y-%m-%d").date()
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def getGender(gender):
    return "M" if gender=="male" else "F"

def userLoggedIn():
    return ('loggedIn' in session)

def userType(type):
    return True

def loginUser(email):
    session['loggedIn'] = True
    session['email'] = email
    session['id'] = getUserID(email)
    session['username'] = getUsername(email)
    session['phone'] = getPhone(email)

def getUsername(email):
    dbCursor = db.cursor()
    sql = "SELECT username FROM login_database WHERE email = %s"
    val = (email, )
    dbCursor.execute(sql,val)
    res = dbCursor.fetchone()[0]
    dbCursor.close()
    return res

def getPhone(email):
    dbCursor = db.cursor()
    sql = "SELECT phone FROM login_database WHERE email = %s"
    val = (email, )
    dbCursor.execute(sql,val)
    res = dbCursor.fetchone()[0]
    dbCursor.close()
    return res

def getUserID(email):
    return '997723'

def addUser(requestForm, tp):
    dbCursor = db.cursor()
    sql = "INSERT INTO login_database (username, password, email, phone) VALUES (%s, %s, %s, %s) "
    val = (requestForm['username'], requestForm['password'], requestForm['email'], requestForm['phone'])
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()
    if tp=='client':
        addClient(requestForm)

def validLogin(email, password):
    dbCursor = db.cursor()
    sql = "SELECT * FROM login_database WHERE email = %s AND password = %s"
    val = (email, password)
    dbCursor.execute(sql, val)
    res = True if dbCursor.fetchone() else False
    dbCursor.close()
    return res


def userExists(requestForm):
    dbCursor = db.cursor()
    sql = "SELECT * FROM login_database WHERE username = %s OR email = %s OR phone = %s"
    val = (requestForm['username'], requestForm['email'], requestForm['phone'])
    dbCursor.execute(sql, val)
    res = True if dbCursor.fetchone() else False
    dbCursor.close()
    return res

def validateSignupRequest(formData):
    return (checkNotPresent('username',formData['username'], 'login_database', 'Username already in use') 
        and checkNotPresent('email',formData['email'], 'login_database', 'Email already in use')
        and checkNotPresent('phone',formData['phone'], 'login_database', 'Phone already in use')
        and checkNotPresent('client_aadhar',formData['aadhar'], 'client_database', 'Aadhar already linked to another account')
        and checkNotPresent('client_PAN',formData['pan'], 'client_database', 'PAN number already linked to another account')
    ) 

def checkNotPresent(attr, val, table, flashMessage=""):
    dbCursor = db.cursor()
    sql = "SELECT * FROM " + table + " WHERE " + attr + " = %s"
    val = (val, )
    dbCursor.execute(sql, val)
    res = False if dbCursor.fetchone() else True
    dbCursor.close()
    if len(flashMessage)>0 and not res:
        flash(flashMessage)
    return res
