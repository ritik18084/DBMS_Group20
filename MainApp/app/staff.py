from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType

staff = Blueprint('staff',__name__)



@staff.route('/staffDashboard')
def dashboard():
    if not(userLoggedIn() and userType('staff')):
        return
    return render_template('staff/dashboard.html')


@staff.route('/staffClientInfo')
def dashboardClient():
    if not(userLoggedIn() and userType('staff')):
        return
    return render_template('staff/clientInfo.html')

@staff.route('/staffInsuranceInfo')
def dashboardInsurance():
    if not(userLoggedIn() and userType('staff')):
        return
    return render_template('staff/insurance.html', staffClientQuery=False)


@staff.context_processor
def viewStaffProfile():
	if not(userLoggedIn() and userType('staff')):
		return
	dbCursor = db.cursor()
	sql = "SELECT A.employee_name," \
	"A.employee_aadhar, A.employee_PAN, B.branch_name,A.department, A.position, A.salary, A.employee_ph FROM STAFF_DATABASE A, BRANCH_DATABASE B " \
	"WHERE employee_ID = %s AND A.branch_ID=B.branch_ID"
	employee_ID = session['id']
	val = (employee_ID,)
	dbCursor.execute(sql, val)
	res = dbCursor.fetchone()
	dbCursor.close()
	return {'staffProfile' : [session['username'], res[7], session['email'], res[0], res[1], res[2],res[3], res[4],res[5],res[6]]}

@staff.route('/viewClientDetails', methods = ["POST"])
def viewClientDetails():
	if not(userLoggedIn() and userType("staff")):
		return
	dbCursor = db.cursor()
	sql = "SELECT A.*,B.*  FROM CLIENT_DATABASE A, AGENT_DATABASE B WHERE A.client_ID = %s AND A.agent_ID=B.agent_ID"
	val = (request.form['clientID'],)
	dbCursor.execute(sql, val)
	res = dbCursor.fetchone()
	sql = "SELECT Unique_Ins_ID, ins_type, end_date  FROM INSURANCE_DATABASE WHERE client_ID = %s"
	val = (request.form['clientID'],)
	dbCursor.execute(sql, val)
	res2 = dbCursor.fetchall()
	dbCursor.close()
	if res:
		return render_template('staff/clientInfo.html',staffClientQuery=True, clientInfo=res, staffClientIns=res2)
	else:
		return render_template('staff/clientInfo.html',staffClientQuery=False)

@staff.route("/viewStaffInsurance", methods = ['POST'])
def viewInsurance():
	if not(userLoggedIn() and userType('staff')):
		return
	dbCursor = db.cursor()
	sql = "SELECT A.*, B.policy_name FROM INSURANCE_DATABASE A, POLICY_DATABASE B WHERE A.Unique_ins_id = %s AND B.policy_key=A.policy_key"
	val = (request.form['insID'],)
	dbCursor.execute(sql, val)
	res = dbCursor.fetchone()
	dbCursor.close()
	if res:
		return render_template('staff/insurance.html',staffInsQuery=True, insInfo=res)
	else:
		return render_template('staff/insurance.html',staffInsQuery=False)
	
	