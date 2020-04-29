from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from . import db
from random import randint
from datetime import datetime, date
import time
auth = Blueprint('auth',__name__)


def generateUID(length=12):
    if length<10:
        uid = ""
        while len(uid) < length:
            uid = uid + str(randint(0,9))
        return uid
    uid = str(int(time.time()))
    while len(uid) < length:
        uid = uid + str(randint(0,9))
    return uid

@auth.route('/login')
def loginPage():
    if userLoggedIn():
        return redirect(url_for('client.dashboard'))
    return render_template('login.html')

@auth.route('/signup')
def signupPage():
    if userLoggedIn():
        return redirect(url_for('main.index'))
    return render_template('signup.html')


@auth.route('/companySignup')
def companySignup():
    if userLoggedIn():
        return redirect(url_for('main.index'))
    return render_template('company_signup.html')

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
        addUser(request.form, tp="client")
        loginUser(request.form['email'])
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.signupPage'))        


@auth.route('/company_signup', methods= ['POST'])
def company_signup():
    if userLoggedIn():
        return redirect(url_for('main.index'))
    if validateCompanySignupRequest(request.form):
        addUser(request.form, tp="organizations")
        loginUser(request.form['email'])
        return openDashboard() 
    return redirect(url_for('auth.company_signup_Page'))


def openDashboard():
    if userType('client'):
        return redirect(url_for('client.dashboard'))
    if userType('shareholders'):
        return redirect(url_for('shareholders.dashboard'))
    if userType('agent'):
        return redirect(url_for('agent.dashboard'))
    if userType('staff'):
        return redirect(url_for('staff.dashboard'))
    if userType('organizations'):
        return redirect(url_for('organizations.dashboard'))
    if userType('admin'):
        return redirect(url_for('admin.dashboard'))

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

def userType(userType):
    return (session['userType'] == userType)

def loginUser(email):
    session['loggedIn'] = True
    session['email'] = email
    session['id'], session['username'], session['userType'] = getUserInfo(email)

def getUserInfo(email):
    dbCursor = db.cursor()
    sql = "SELECT user_type, username FROM login_database WHERE email = %s"
    val = (email, )
    dbCursor.execute(sql,val)
    res = dbCursor.fetchone()
    usertype = res[0]
    username = res[1]
    userId = 0
    if usertype == 'client':
        sql = "SELECT client_ID FROM client_database WHERE client_email = %s"
        val = (email,)
        dbCursor.execute(sql,val)
        userID = dbCursor.fetchone()[0]
    elif usertype == 'staff':
        sql = "SELECT employee_ID FROM staff_database WHERE employee_email = %s"
        val = (email,)
        dbCursor.execute(sql,val)
        userID = dbCursor.fetchone()[0]
    elif usertype == 'agent':
        sql = "SELECT agent_ID FROM agent_database WHERE agent_email = %s"
        val = (email,)
        dbCursor.execute(sql,val)
        userID = dbCursor.fetchone()[0]
    elif usertype == 'shareholders':
        sql = "SELECT share_ID FROM shareholders_database WHERE share_email = %s"
        val = (email,)
        dbCursor.execute(sql,val)
        userID = dbCursor.fetchone()[0]
    elif usertype == 'organizations':
        sql = "SELECT company_ID FROM company_database WHERE company_email = %s"
        val = (email,)
        dbCursor.execute(sql,val)
        userID = dbCursor.fetchone()[0]

    dbCursor.close()
    return userID, username, usertype


def addUser(requestForm, tp=""):
    dbCursor = db.cursor()
    sql = "INSERT INTO login_database (username, password, email, phone, user_type) VALUES (%s, %s, %s, %s, %s) "
    val = (requestForm['username'], requestForm['password'], requestForm['email'], requestForm['phone'], tp)
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()
    if tp=='client':
        addClient(requestForm)
    if tp=='organizations':
        addCompany(requestForm)

def validLogin(email, password):
    dbCursor = db.cursor()
    sql = "SELECT * FROM login_database WHERE email = %s AND password = %s"
    val = (email, password)
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

############

#COMPANY SIGNUP
def validateCompanySignupRequest(formData):
    return ( checkNotPresent('username',formData['username'], 'login_database', 'Username already in use')
        and checkNotPresent('email',formData['email'], 'login_database', 'Email already in use')
        and checkNotPresent('phone',formData['phone'], 'login_database', 'Phone already in use')
        and checkNotPresent('company_reg_no',formData['regNo'], 'company_database', 'Registration no linked to another account')
    )

def addCompany(requestForm):
    dbCursor = db.cursor()
    sql = "INSERT INTO company_database VALUES (%s, %s, %s, %s, %s, %s, 0, %s, %s, %s)"
    val = (requestForm['name'], requestForm['regNo'], 
    requestForm['email'], requestForm['collab_type'],
    requestForm['duration'],requestForm['phone'], 
    requestForm['discount'], requestForm['type'],
    generateUID(12))
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()


############

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


