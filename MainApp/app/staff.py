from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType

staff = Blueprint('staff',__name__)

@staff.route('/viewstaffprofile', methods= ['POST'])
def viewsold():
    if not(userLoggedIn() and userType('staff')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM staff_database WHERE employee_ID=%s"
    val = (session['id'])
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return res

