from flask import Blueprint, session, request, redirect, url_for, render_template
from . import db
from .auth import userLoggedIn,userType

client = Blueprint('client',__name__)

@client.route('/viewclientprofile', methods= ['POST'])
def viewprofile():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT client_name, client_ph, client_email, client_aadhar, \
    client_PAN, client_DOB FROM client_database WHERE client_ID=%s"
    val = (session['id'],)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return res


@client.route('/viewallpolicies', methods= ['POST'])
def viewallpolicies():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT policy_name, ins_type, min_coverage, premium,eligibility_cond,\
    terms_conditions FROM policy_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchall()
    dbCursor.close()
    return res

@client.route('/viewinsurances', methods= ['POST'])
def viewinsurances():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT * FROM insurance_database WHERE client_ID = %s"
    val = (session['id'],)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return res

@client.route('/boughtInsurance', methods=['POST'])
def boughtInsurance():
	if not(userLoggedIn() and userType('client')):
		return

	dbCursor = db.cursor()

	sql = "INSERT INTO insurance_database values(client_name\
	, ins_type, policy_key, coverage_amt, ppm, client_ID, agent_ID, GETDATE(),\
	GETDATE + duration, premium, employee_ID, branch_ID, Uniq_Ins_ID, dues) \
	SELECT client_name, ins_type, policy_key, coverage_amt, premium/duration, \
	client_ID, agent_ID, GETDATE(), GETDATE() + duration, premium, \
	employee_ID_KAHAse-lau?, branch_ID, get_uniq_ins_id(), 0 FROM \
	client_database, policy_database WHERE client_ID=%s and policy_key=%s"

	client_ID = session["id"]
	policy_key = session["policy_key"]

	dbCursor.execute(sql, (client_ID, policy_key))

	res = dbCursor.fetchall()
	dbCursor.close()
	return res

@client.route("/paydue", methods =['POST'])
def paydue():
	if not(userLoggedIn() and userType('client')):
		return
	dbCursor = db.cursor()

	sql = "TODO"
	val = ()
	dbCursor.execute(sql,val)
	dbCursor.close()

