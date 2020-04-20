from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from random import randint

auth = Blueprint('auth',__name__)



@auth.route('/login')
def loginPage():
    if userLoggedIn():
        return redirect(url_for('main.index'))
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
    if validLogin(request.form['username'], request.form['password']):
        loginUser(request.form['email'])
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.loginPage'))

@auth.route('/signup', methods= ['POST'])
def signup():
    if userLoggedIn():
        return redirect(url_for('main.index'))
    if validateSignupRequest(request.form):
        if userExists(request.form):
            return redirect(url_for('auth.loginPage'))
        addUser(request.form)
        loginUser(request.form['email'])
        return redirect(url_for('main.index'))
    return redirect(url_for('auth.signupPage'))        


def userLoggedIn():
    return ('loggedIn' in session)

def userType(type):
    return True

def loginUser(email):
    session['loggedIn'] = True
    session['email'] = email
    session['id'] = getUserID()


def getUserID(email):
    return 12345

def addUser(requestForm):
    dbCursor = db.cursor()
    sql = "INSERT INTO login_database (username, password, email, phone) VALUES (%s, %s, %s, %s) "
    val = (requestForm['username'], requestForm['password'], requestForm['email'], requestForm['phone'])
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()

def validLogin(username, password):
    dbCursor = db.cursor()
    sql = "SELECT * FROM login_database WHERE username = %s AND password = %s"
    val = (username, password)
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
    return (validUsername(formData['username']) 
        and validPassword(formData['password'])
        and validEmail(formData['email'])
        and validPhone(formData['phone'])
    ) 

def validUsername(username):
    return isinstance(username, str) and len(username) > 1

def validPassword(password):
    return isinstance(password, str) and len(password) > 1

def validEmail(email):
    return isinstance(email, str) and len(email) > 1

def validPhone(ph):
    return isinstance(ph, str) and ph.isdigit() and len(ph) == 10