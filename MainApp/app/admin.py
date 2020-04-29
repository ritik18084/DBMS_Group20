import time
from random import randint
from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from . import db
from .auth import userLoggedIn, userType, addUser, generateUID, checkNotPresent
from datetime import datetime

admin = Blueprint('admin',__name__)

# COMMON TO SHAREHOLDERS
@admin.app_context_processor
def viewBranchDetails():
    # if not(userLoggedIn() and (userType('admin') or userType('shareholders'))):
    #     return
    dbCursor = db.cursor()
    sql = "SELECT * FROM branch_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'branchDetails' :  res}


@admin.route('/adminDashboard')
def dashboard():
    if not(userLoggedIn() and userType('admin')):
        return
    return render_template('admin/dashboard.html')



@admin.route('/adminBranchEmp')
def dashboardBranchEmp():
    if not(userLoggedIn() and userType('admin')):
        return
    return render_template('admin/branchEmp.html',branchEmpQuery=False)
    

@admin.route('/adminDeactivate')
def dashboardDeactivateAcc():
    if not(userLoggedIn() and userType('admin')):
        return
    return render_template('admin/deactivateAccount.html')


@admin.route('/adminAddAgent')
def dashboardAddAgent():
    if not(userLoggedIn() and userType('admin')):
        return
    return render_template('admin/dashboardAddAg.html')


@admin.route('/adminAddEmp')
def dashboardAddEmp():
    if not(userLoggedIn() and userType('admin')):
        return
    return render_template('admin/dashboardAddEmp.html')
    



@admin.context_processor
def viewLogins():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM login_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'allLogins' : res}

@admin.route('/removeLogin', methods=['POST'])
def remLogin():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    email = request.form['ID']
    sql = "DELETE FROM login_database WHERE email=%s"
    val=(email, )
    dbCursor.execute(sql,val)
    db.commit()
    dbCursor.close()
    return redirect(url_for('admin.dashboardDeactivateAcc'))


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
    if validateAddStaffRequest(request.form):
        addUser(request.form, "staff")
        sql = "INSERT INTO staff_database VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (request.form['name'], request.form['phone'], 
        request.form['email'], request.form['aadhar'],
        request.form['pan'], generateUID(12),
        request.form['branch'], request.form['dept'],
        request.form['pos'], request.form['salary'])
        dbCursor.execute(sql, val)
        db.commit()
        dbCursor.close()
    flash("Successfully Registered!","success")
    return redirect(url_for('admin.dashboardAddEmp'))

@admin.route('/addAgent', methods= ['POST'])
def addAgent():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    if validateAddAgentRequest(request.form):
        addUser(request.form, "agent")
        sql = "INSERT INTO agent_database VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (request.form['name'], request.form['phone'], 
        request.form['email'], request.form['aadhar'],
        generateUID(12),'0', request.form['commission'],
        request.form['benefit'])
        dbCursor.execute(sql, val)
        db.commit()
        dbCursor.close()
    flash("Successfully Registered!","success")
    return redirect(url_for('admin.dashboardAddAgent'))

def validateAddAgentRequest(formData):
    return (checkNotPresent('username',formData['username'], 'login_database', 'Username already in use') 
        and checkNotPresent('email',formData['email'], 'login_database', 'Email already in use')
        and checkNotPresent('phone',formData['phone'], 'login_database', 'Phone already in use')
        and checkNotPresent('agent_aadhar',formData['aadhar'], 'agent_database', 'Aadhar already linked to another account')
    ) 

def validateAddStaffRequest(formData):
    return (checkNotPresent('username',formData['username'], 'login_database', 'Username already in use') 
        and checkNotPresent('email',formData['email'], 'login_database', 'Email already in use')
        and checkNotPresent('phone',formData['phone'], 'login_database', 'Phone already in use')
        and checkNotPresent('employee_aadhar',formData['aadhar'], 'staff_database', 'Aadhar already linked to another account')
        and checkNotPresent('employee_PAN',formData['pan'], 'staff_database', 'PAN already linked to another account')
    ) 


@admin.context_processor
def checkProfit():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT A.branch_ID, B.branch_name,SUM(A.P) as profit FROM " \
        "(SELECT branch_ID, SUM(premium-coverage_amt) as P FROM insurance_database WHERE end_date <= %s GROUP BY branch_ID UNION ALL " \
        "SELECT branch_ID, SUM(TIMESTAMPDIFF(MONTH, start_date, %s)*ppm) as P FROM insurance_database WHERE end_date > %s GROUP BY branch_ID UNION ALL " \
        "SELECT branch_ID, 0 as P FROM branch_database) AS A, branch_database B " \
        "WHERE A.branch_ID = B.branch_ID GROUP BY A.branch_ID"
    val = (currDate, currDate, currDate)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    print(res)
    return {'branchProfit' : res}


@admin.route('/viewbranchStaff', methods= ['POST'])
def viewbranchStaff():
    if not(userLoggedIn() and userType('admin')):
        return
    dbCursor = db.cursor()
    branchID = request.values.get('branchID')
    sql = "SELECT * FROM staff_database WHERE branch_ID = %s "
    val = (branchID, )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    if res:
        return render_template('admin/branchEmp.html', branchEmpQuery=True, branchEmp=res)
    else:
        return render_template('admin/branchEmp.html', branchEmpQuery=False)






