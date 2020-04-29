from flask import Blueprint, session, request, redirect, url_for, render_template, flash
from . import db
from .auth import userLoggedIn, userType, generateUID
from datetime import datetime
from werkzeug.utils import secure_filename
import os

client = Blueprint('client',__name__)

@client.route('/clientDashboard')
def dashboard():
    if not(userLoggedIn() and userType('client')):
        return
    return render_template('client/dashboard.html')

@client.route('/clientInsurances')
def dashboardInsurances():
    if not(userLoggedIn() and userType('client')):
        return
    return render_template('client/insurance.html')

@client.route('/clientViewPolicies')
def dashboardViewPolicies():
    if not(userLoggedIn() and userType('client')):
        return
    return render_template('client/policies.html')

@client.route('/buyInsurance')
def dashboardBuy():
    if not(userLoggedIn() and userType('client')):
        return
    return render_template('client/buy.html')

@client.route('/payDues')
def dashboardPayDues():
    if not(userLoggedIn() and userType('client')):
        return
    return render_template('client/pay.html')

@client.route('/transactionHistory')
def dashboardHistory():
    if not(userLoggedIn() and userType('client')):
        return
    return render_template('client/history.html')


@client.context_processor
def viewprofile():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT A.*, B.agent_name, B.agent_ph, B.agent_email, C.branch_name FROM client_database A, agent_database B, branch_database C WHERE A.client_ID=%s AND A.agent_ID = B.agent_ID AND A.branch_ID = C.branch_ID" 
    val = (session['id'],)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'clientInfo' : [session['username'], res[1], session['email'], res[0], res[3], res[4], res[7], res[8], res[9], res[13], res[14], res[15], res[16] ]}


@client.context_processor
def viewBuyPolicies():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT ins_type,policy_name,policy_key, min_coverage, premium, duration_min, eligibility_cond,\
    terms_conditions FROM policy_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'buyPolicies' : res}

@client.context_processor
def viewallpolicies():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT policy_name, ins_type, min_coverage, premium,eligibility_cond,\
    terms_conditions FROM policy_database"
    dbCursor.execute(sql)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'allPolicies' : res}

@client.context_processor
def viewallTransactions():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT A.payment_datetime, A.amount, B.Unique_Ins_ID, C.ins_type, C.policy_name \
    FROM TRANSACTIONS A, INSURANCE_DATABASE B, POLICY_DATABASE C \
    WHERE A.Unique_Ins_ID = B.Unique_Ins_ID AND B.client_ID = %s AND C.policy_key = B.policy_key \
    ORDER BY A.payment_datetime DESC"
    val = (session['id'], )
    dbCursor.execute(sql,val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'allTransactions' : res}


@client.context_processor
def totalInsurances():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT COUNT(*) FROM insurance_database WHERE client_ID = %s";
    val = (session['id'], )
    dbCursor.execute(sql,val)
    res = dbCursor.fetchone()
    dbCursor.close()
    return {'totalInsurances' : res}

@client.context_processor
def viewinsurances():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT B.policy_name, B.ins_type, B.min_coverage, B.premium, A.start_date, B.duration_min, A.ppm, A.dues \
        FROM insurance_database A, policy_database B WHERE A.client_ID = %s AND A.policy_key = B.policy_key"
    val = (session['id'],)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'allInsurances' : res}

@client.context_processor
def offers():
    if not(userLoggedIn() and userType('client')):
        return
    return {'offerValid' : False}


@client.context_processor
def getDues():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    sql = "SELECT B.policy_name, B.min_coverage,B.premium, A.dues, A.Unique_ins_ID \
        FROM insurance_database A, policy_database B WHERE A.client_ID = %s AND A.policy_key = B.policy_key AND A.dues > 0"
    val = (session['id'],)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchall()
    dbCursor.close()
    return {'dues' : res}

@client.route("/paydue", methods =['POST'])
def paydue():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    currDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    sql = "SELECT dues FROM insurance_database WHERE Unique_Ins_ID = %s"
    val = (request.form['id'],)
    dbCursor.execute(sql,val)
    res = dbCursor.fetchone()
    if res:
        amount = res[0]
        sql = "INSERT INTO TRANSACTIONS VALUES ('%s', '%s', %f, '%s')" % (generateUID(16),request.form['id'],amount,currDateTime)
        dbCursor.execute(sql)
        db.commit()
        sql = "UPDATE insurance_database SET dues=0 WHERE Unique_Ins_ID = %s"
        val = (request.form['id'], )
        dbCursor.execute(sql,val)
        db.commit()
        dbCursor.close()
        flash('Transaction Successful')
        return redirect(url_for('client.dashboardPayDues'))


@client.route('/buyInsurance', methods=['POST'])
def boughtInsurance():
    if not(userLoggedIn() and userType('client')):
        return
    dbCursor = db.cursor()
    policy_key = request.form['policy_key']
    sql = "SELECT ins_type FROM policy_database WHERE policy_key=%s"
    val = (policy_key,)
    dbCursor.execute(sql, val)
    res = dbCursor.fetchone()
    dbCursor.close()
    if not res:
        return
    insType = res[0]
    if insType == "Home":
        return buyHome(request)
    elif insType == "Vehicle":
        return buyVehicle(request)
    elif insType == "Medical":
        return buyMedical(request)
    elif insType == "Travel":
        return buyTravel(request)
    else:
        return buyLife(request)


def buyHome(req):
    dbCursor = db.cursor()
    # INSERT INTO INSURANCE DATABASE AND STORE UNIQUE INS ID
    unique_ins_id = '634736195656'
    path = unique_ins_id
    # sql = "INSERT INTO INSURANCE_DATABASE VALUES "
     
    if 'file' not in req.files:
        flash('No file Provided')
        return redirect(url_for('client.dashboardBuy'))
    file = req.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('client.dashboardBuy'))
    if file:
        filename = secure_filename(file.filename)
        file.save(path)
        sql = "INSERT INTO home_insurance_database VALUES ('%s', '%s', '%s', %d, '%s')" \
            % (unique_ins_id, req.form['location'],path,int(req.form['area']), req.form['ownerName'])
        dbCursor.execute(sql)
        db.commit()
        dbCursor.close()
        flash('Purchase Successfull')
        return redirect(url_for('client.dashboardBuy'))

    flash('No selected file')
    return redirect(url_for('client.dashboardBuy'))
    

def buyVehicle(req):
    dbCursor = db.cursor()
    # INSERT INTO INSURANCE DATABASE AND STORE UNIQUE INS ID
    unique_ins_id = '634736195656'
    path = unique_ins_id
    # sql = "INSERT INTO INSURANCE_DATABASE VALUES "

    sql = "SELECT * FROM vehicle_insurance_database WHERE RC_num = %s" \
        % (req.form['rcno'])
    dbCursor.execute(sql)
    res = dbCursor.fetchone()
    
    if res:
        flash('RC already linked to another insurance')
        return redirect(url_for('client.dashboardBuy')) 
    
    if 'file' not in req.files:
        flash('No file Provided')
        return redirect(url_for('client.dashboardBuy'))
    file = req.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('client.dashboardBuy'))
    if file:
        filename = secure_filename(file.filename)
        file.save(path)
        sql = "INSERT INTO vehicle_insurance_database (Unique_Ins_ID, vehicle_ID, vehicle_type, RC_num, Path_to_RC)" \
            "VALUES ('%s', '%s', '%s', '%s', '%s')" \
            % (unique_ins_id, req.form['vehicleID'], req.form['type'],req.form['rcno'],path)
        dbCursor.execute(sql)
        db.commit()
        dbCursor.close()
        flash('Purchase Successfull')
        return redirect(url_for('client.dashboardBuy'))

    flash('No selected file')
    return redirect(url_for('client.dashboardBuy'))

def buyTravel(req):
    dbCursor = db.cursor()
    # INSERT INTO INSURANCE DATABASE AND STORE UNIQUE INS ID
    unique_ins_id = '138515833433'
    # sql = "INSERT INTO INSURANCE_DATABASE VALUES "
    sql = "INSERT INTO travel_insurance_database VALUES ('%s','%s', '%s', '%s')" \
        % (unique_ins_id, req.form['date'], req.form['travelType'], req.form['details'])
    dbCursor.execute(sql)
    db.commit()
    dbCursor.close()
    flash('Purchase Successfull')
    return redirect(url_for('client.dashboardBuy'))

def buyLife(req):
    dbCursor = db.cursor()
    # INSERT INTO INSURANCE DATABASE AND STORE UNIQUE INS ID
    unique_ins_id = '634736195656'
    path = unique_ins_id
    # sql = "INSERT INTO INSURANCE_DATABASE VALUES "
     
    if 'file' not in req.files:
        flash('No file Provided')
        return redirect(url_for('client.dashboardBuy'))
    file = req.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('client.dashboardBuy'))
    if file:
        filename = secure_filename(file.filename)
        file.save(path)
        sql = "INSERT INTO life_insurance_database VALUES ('%s', '%s', '%s', '%s')" \
            % (unique_ins_id, req.form['nom1name'], req.form['nom2name'],path)
        dbCursor.execute(sql)
        db.commit()
        dbCursor.close()
        flash('Purchase Successfull')
        return redirect(url_for('client.dashboardBuy'))

    flash('No selected file')
    return redirect(url_for('client.dashboardBuy'))

def buyMedical(req):
    dbCursor = db.cursor()
    # INSERT INTO INSURANCE DATABASE AND STORE UNIQUE INS ID
    unique_ins_id = '634736195656'
    path = unique_ins_id
    # sql = "INSERT INTO INSURANCE_DATABASE VALUES "
     
    if 'file' not in req.files:
        flash('No file Provided')
        return redirect(url_for('client.dashboardBuy'))
    file = req.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('client.dashboardBuy'))
    if file:
        filename = secure_filename(file.filename)
        file.save(path)
        sql = "INSERT INTO medical_insurance_database VALUES ('%s', '%s', '%s')" \
            % (unique_ins_id, req.form['history'],path)
        dbCursor.execute(sql)
        db.commit()
        dbCursor.close()
        flash('Purchase Successfull')
        return redirect(url_for('client.dashboardBuy'))

    flash('No selected file')
    return redirect(url_for('client.dashboardBuy'))

