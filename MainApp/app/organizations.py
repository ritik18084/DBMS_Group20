from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType

organizations = Blueprint('organizations',__name__)


@organizations.route('/orgDashboard')
def dashboard():
    if not(userLoggedIn() and userType('organizations')):
        return
    return render_template('organization/dashboard.html')

@organizations.route('/orgClients')
def dashboardClients():
    if not(userLoggedIn() and userType('organizations')):
        return
    return render_template('organization/clientInfo.html')

@organizations.route('/orgCollab')
def dashboardCollab():
    if not(userLoggedIn() and userType('organizations')):
        return
    return render_template('organization/collab.html')


@organizations.context_processor
def viewOrgProfile():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    company_ID = session['id']
    sql = "SELECT * FROM company_database WHERE company_ID = %s "
    val = (company_ID, )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'orgProfile' : [session['username'], res[5], session['email'], res[0], res[1], res[7]]}

@organizations.context_processor
def viewOrgNumberClients():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "SELECT COUNT(*) FROM client_database A, company_database B WHERE A.company_reg_no = B.company_reg_no AND B.company_ID = %s "
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'orgClientCount' : res}

@organizations.context_processor
def viewOrgClients():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "SELECT A.client_name, A.client_ph, A.client_email FROM client_database A, company_database B WHERE A.company_reg_no = B.company_reg_no AND B.company_ID = %s "
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'orgClients' : res}



@organizations.context_processor
def viewCollabDetails():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "SELECT collab_type, collab_date, collab_duration FROM company_database WHERE company_ID = %s "
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'collabDetails' : res}


@organizations.route('/extendCollabDuration', methods= ['POST'])
def extendCollabDuration():
    if not(userLoggedIn() and userType('organizations')):
        return
    dbCursor = db.cursor()
    sql = "UPDATE company_database SET collab_duration = collab_duration + " + str(int(request.form['extension'])) + " WHERE company_ID = %s "
    val = (session['id'],)
    print(val)
    print(sql)
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()
    return redirect(url_for('organizations.dashboardCollab'))

