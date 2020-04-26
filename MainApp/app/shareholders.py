from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType
from datetime import datetime

shareholders = Blueprint('shareholders',__name__)


@shareholders.route('/shareDashboard')
def dashboard():
    if not(userLoggedIn() and userType('shareholders')):
        return
    return render_template('shareholders/dashboard.html')

@shareholders.route('/shareProfit')
def dashboardProfit():
    if not(userLoggedIn() and userType('shareholders')):
        return
    return render_template('shareholders/profit.html')

@shareholders.route('/shareStats')
def dashboardStats():
    if not(userLoggedIn() and userType('shareholders')):
        return
    return render_template('shareholders/stats.html')

@shareholders.route('/shareBranch')
def dashboardBranch():
    if not(userLoggedIn() and userType('shareholders')):
        return
    return render_template('shareholders/branch.html')   

@shareholders.route('/activeInsurances', methods= ['POST'])
def activeInsurances():
    if not(userLoggedIn() and userType('shareholders')):
        return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT COUNT(*) AS count FROM insurance_database WHERE end_date > %s"
    val = (currDate, )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchOne()
    dbCursor.close()
    return res

@shareholders.app_context_processor
def activeInsuranceCounts():
    # if not(userLoggedIn() and userType('shareholders')):
    #     return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT COUNT(*) AS count FROM insurance_database WHERE end_date > %s"
    val = (currDate, )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'activeInsurances' : res}


@shareholders.app_context_processor
def howManyactiveXYZ():
    # if not(userLoggedIn() and userType('shareholders')):
    #     return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT ins_type, COUNT(*) AS count FROM insurance_database WHERE end_date > %s GROUP BY ins_type"
    val = (currDate, )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'activeXYZ' : res}



@shareholders.app_context_processor
def totalInsuranceCounts():
    # if not(userLoggedIn() and userType('shareholders')):
    #     return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT COUNT(*) AS count FROM insurance_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'totalInsurances' : res}


@shareholders.app_context_processor
def howManytotalXYZ():
    # if not(userLoggedIn() and userType('shareholders')):
    #     return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT ins_type, COUNT(*) AS count FROM insurance_database GROUP BY ins_type"
    dbCursor.execute(sql)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'totalXYZ' : res}



@shareholders.app_context_processor
def getAnnualProfit():
    years = [2015,2016,2017,2018,2019]
    res = []
    for year in years:
        res.append((year,int(annualProfit(year)[0])))
    return {'annualProfit' : res}

def annualProfit(year):
    dbCursor = db.cursor()
    startDate = '%d-01-01' %(year)
    endDate = '%d-12-31' %(year)
    sql = "SELECT SUM(A.P) as profit FROM " \
        "(SELECT SUM(-1*coverage_amt) as P FROM insurance_database WHERE end_date <= %s and end_date >= %s UNION ALL " \
        "SELECT SUM(TIMESTAMPDIFF(MONTH, %s, end_date)*ppm) as P FROM insurance_database WHERE end_date <= %s AND end_date >= %s UNION ALL " \
        "SELECT SUM(12*ppm) as P FROM insurance_database WHERE start_date <= %s AND end_date >= %s UNION ALL " \
        "SELECT SUM(TIMESTAMPDIFF(MONTH, start_date, %s)*ppm) as P FROM insurance_database WHERE start_date >= %s AND start_date <= %s AND end_date >= %s UNION ALL " \
        "SELECT 0 as P FROM insurance_database ) AS A " 
    val = (endDate, startDate, startDate, endDate, startDate, startDate, endDate, endDate, startDate, endDate, endDate)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    print(res)
    dbCursor.close()
    return res

@shareholders.app_context_processor
def netProfit():
    # if not(userLoggedIn() and userType('shareholders')):
    #     return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT SUM(A.P) as profit FROM " \
        "(SELECT SUM(premium-coverage_amt) as P FROM insurance_database WHERE end_date <= %s UNION ALL " \
        "SELECT SUM(TIMESTAMPDIFF(MONTH, start_date, %s)*ppm) as P FROM insurance_database WHERE end_date > %s) AS A" 
    val = (currDate, currDate, currDate)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'netProfit' : (int(res[0]),)}

@shareholders.context_processor
def viewShareProfile():
    # if not(userLoggedIn() and userType('shareholders')):
    #     return
    dbCursor = db.cursor()
    sql = "SELECT equity_percentage, share_name FROM shareholders_database WHERE share_ID = %s"
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'shareUserProfile' : [session['username'], session['phone'], session['email'], res[1], res[0]]}


