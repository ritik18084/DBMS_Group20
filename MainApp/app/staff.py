from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType

staff = Blueprint('staff',__name__)

@staff.route('/viewStaffProfile', methods= ['POST'])

def viewStaffProfile():
	if not(userLoggedIn() and userType('staff')):
		return
	dbCursor = db.cursor()
	sql = "SELECT employee_name, employee_ph, employee_email, \
	employee_aadhar, employee_PAN, department FROM STAFF_DATABASE \
	WHERE employee_ID = %s"

	employee_ID = session['id']
	val = (employee_ID,)
	dbCursor.execute(sql, val)
	res = dbCursor.fetchone()
	dbCursor.close()
	return res

@staff.route('viewClientDetails', methods = ["POST"])

def viewClientDetails():
	if not(userLoggedIn() and userType("staff")):
		return
	dbCursor = db.cursor()
	sql = "SELECT * FROM CLIENT_DATABASE WHERE client_ID = %s"
	val = (session['client_ID'],)
	dbCursor.execute(sql, val)
	res = dbCursor.fetchall()
	dbCursor.close()
	return res

@staff.route("viewInsurance", methods = ['POST'])

def viewInsurance():
	if not(userLoggedIn() and userType('staff')):
		return
	dbCursor = db.cursor()
	sql = "SELECT * FROM INSURANCE_DATABASE WHERE Unique_ins_id = %s"
	val = (session["ins_id"],)
	dbCursor.execute(sql, val)
	res = dbCursor.fetchall()
	return res
	