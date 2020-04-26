from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType

organizations = Blueprint('organizations',__name__)

@organizations.route('/viewOrgProfile', methods= ['POST'])
def viewOrgProfile():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM company_database WHERE company_ID = %s "
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchOne()
    dbCursor.close()
    return res

@organizations.route('/viewOrgNumberClients', methods= ['POST'])
def viewOrgNumberClients():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "SELECT enrolled_customers FROM company_database WHERE company_ID = %s "
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchOne()
    dbCursor.close()
    return res

@organizations.route('/viewOrgClients', methods= ['POST'])
def viewOrgClients():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "SELECT A.client_name, A.client_ph, A.client_email FROM client_database A, company_database B WHERE A.company_reg_no = B.company_reg_no AND B.company_ID = %s "
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res

@organizations.route('/viewCollabDetails', methods= ['POST'])
def viewCollabDetails():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "SELECT collab_type, collab_duration, offers FROM company_database WHERE company_ID = %s "
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res


@organizations.route('/extendCollabDuration', methods= ['POST'])
def extendCollabDuration():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "UPDATE company_database SET collab_duration = %d WHERE company_ID = %s "
    val = (request.values.get('duration'), session['id'] )
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()
    return

