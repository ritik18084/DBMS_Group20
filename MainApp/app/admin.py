import time
from random import randint
from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn, userType, addUser
from datetime import datetime

admin = Blueprint('admin',__name__)

# COMMON TO SHAREHOLDERS
@admin.route('/viewBranchDetails', methods= ['POST'])
def viewBranchDetails():
    if not(userLoggedIn() and (userType('admin') or userType('shareholders'))):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM branch_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res



@admin.route('/viewClients', methods= ['POST'])
def viewClients():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM client_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res

@admin.route('/viewAgents', methods= ['POST'])
def viewAgents():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM agent_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res

@admin.route('/viewStaff', methods= ['POST'])
def viewStaff():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM staff_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res

@admin.route('/viewOrgs', methods= ['POST'])
def viewOrgs():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM company_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res


@admin.route('/deleteClient', methods= ['POST'])
def deleteClient():
    if not(userLoggedIn() and userType('admin')):
        return
    deleteID = request.values.get('ID')
    dbCursor = db.cursor()
    sql = "DELETE FROM client_database WHERE client_ID = %s"
    val = (deleteID, )
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()
    
@admin.route('/deleteAgent', methods= ['POST'])
def deleteAgent():
    if not(userLoggedIn() and userType('admin')):
        return
    deleteID = request.values.get('ID')
    dbCursor = db.cursor()
    sql = "DELETE FROM agent_database WHERE agent_ID = %s"
    val = (deleteID, )
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()

@admin.route('/deleteStaff', methods= ['POST'])
def deleteStaff():
    if not(userLoggedIn() and userType('admin')):
        return
    deleteID = request.values.get('ID')
    dbCursor = db.cursor()
    sql = "DELETE FROM staff_database WHERE employee_ID = %s"
    val = (deleteID, )
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()

@admin.route('/deleteOrg', methods= ['POST'])
def deleteOrg():
    if not(userLoggedIn() and userType('admin')):
        return
    deleteID = request.values.get('ID')
    dbCursor = db.cursor()
    sql = "DELETE FROM company_database WHERE company_ID = %s"
    val = (deleteID, )
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()

def generateUID(length=12):
    uid = str(int(time.time()))
    while len(uid) < length:
        uid = uid + str(randint(0,9))
    return uid

@admin.route('/addStaff', methods= ['POST'])
def addStaff():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    addUser(request.form)
    sql = "INSERT INTO staff_database VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (request.form['name'], request.form['phone'], 
    request.form['email'], request.form['aadhar'],
    request.form['pan'], generateUID(12),
    request.form['branch_id'], request.form['dept'],
    request.form['pos'], request.form['salary'])
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()

@admin.route('/addAgent', methods= ['POST'])
def addAgent():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    addUser(request.form)
    sql = "INSERT INTO agent_database VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (request.form['name'], request.form['phone'], 
    request.form['email'], request.form['aadhar'],
    generateUID(12),'0', request.form['commission'],
    request.form['benefit'])
    dbCursor.execute(sql, val)
    db.commit()
    dbCursor.close()

@admin.route('/checkProfit', methods= ['POST'])
def checkProfit():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT branch_ID, SUM(A.P) as profit FROM " \
        "(SELECT branch_ID, SUM(premium-coverage_amt) as P FROM insurance_database WHERE end_date <= %s GROUP BY branch_ID UNION ALL " \
        "SELECT branch_ID, SUM(TIMESTAMPDIFF(MONTH, start_date, %s)*ppm) as P FROM insurance_database WHERE end_date > %s GROUP BY branch_ID UNION ALL " \
        "SELECT branch_ID, 0 as P FROM branch_database) AS A " \
        "GROUP BY branch_ID"
    val = (currDate, currDate, currDate)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res

@admin.route('/totalPoiliciesBranch', methods= ['POST'])
def totalPoiliciesBranch():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    sql = "SELECT branch_ID, branch_name, policies_enrolled from branch_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res

@admin.route('/viewbranchStaff', methods= ['POST'])
def viewStaff():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    branchID = request.values.get('ID')
    sql = "SELECT * FROM staff_database WHERE branch_ID = %s "
    val = (branchID, )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchAll()
    dbCursor.close()
    return res





