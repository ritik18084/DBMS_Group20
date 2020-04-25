from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType
from datetime import datetime

shareholders = Blueprint('shareholders',__name__)

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

@shareholders.route('/howManyXYZ', methods= ['POST'])
def howManyXYZ():
    if not(userLoggedIn() and userType('shareholders')):
        return
    dbCursor = db.cursor()
    currDate = datetime.today().strftime('%Y-%m-%d')
    sql = "SELECT COUNT(*) AS count FROM insurance_database WHERE end_date > %s GROUP BY ins_type"
    val = (currDate, )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return res


@shareholders.route('/annualProfit', methods= ['POST'])
def annualProfit():
    if not(userLoggedIn() and userType('shareholders')):
        return
    dbCursor = db.cursor()
    year = int(request.values.get('year'))
    startDate = '%d-01-01' %(year)
    endDate = '%d-12-31' %(year)
    sql = "SELECT SUM(A.P) as profit FROM " \
        "(SELECT SUM(-1*coverage_amt) as P FROM insurance_database WHERE end_date <= %s and end_date >= %s UNION ALL " \
        "SELECT SUM(TIMESTAMPDIFF(MONTH, %s, end_date)*ppm) as P FROM insurance_database WHERE end_date <= %s AND end_date >= %s UNION ALL " \
        "SELECT SUM(12*ppm) as P FROM insurance_database WHERE start_date <= %s AND end_date >= %s UNION ALL " \
        "SELECT SUM(TIMESTAMPDIFF(MONTH, start_date, %s)*ppm) as P FROM insurance_database WHERE start_date >= %s AND start_date <= %s AND end_date >= %s) AS A " 
    val = (endDate, startDate, startDate, endDate, startDate, startDate, endDate, endDate, startDate, endDate, endDate)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchOne()
    dbCursor.close()
    return res

@shareholders.route('/viewShareProfile', methods= ['POST'])
def viewShareProfile():
    if not(userLoggedIn() and userType('shareholders')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM shareholders_database WHERE share_ID = %s"
    val = (session['id'], )
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return res


