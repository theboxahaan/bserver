from flask import Flask
from flask import request, jsonify, make_response, g
from pprint import pprint
import qr
import dbcon
from werkzeug.datastructures import MultiDict
import os, sys
import secrets
from login import login_required

app = Flask(__name__)

#declare root route

@app.route('/')
def index():
    return '<h1>Hello World</h1>'

#routes witha a dynamic component
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello %s </h1>' % name



#define a REST endpoint. If a POST request is submitted to this endpoint with a validated token(type int), then a QR code is received.

#Since this is a RESTful api, each request should contain complete data to compute the response, i.e. no state should be maintained. Each request to the get_qr should contain  - a.Session_ID <for identification & authentication>  b.Payees A/C Name or A/C number c.Amount of Transaction d.Addtional Remarks e.TXID


#@app.route('/api/get_qr_test', methods = ['POST', 'GET'])
#def get_qr():
    #if request.method == 'POST':
        #return jsonify(request.args)
        #pprint(vars(request.values.dicts))
        #pprint(request.json)
        #pprint(request.data)
        #file  = open('test.pem', 'wb')
        #file.write(request.data)
        #return "1"
        #return jsonify({"Okay":"Done"})

        #return make_response(request.charset)
    #else: return "Improper Request"
    


@app.route('/api/get_qr', methods = ['POST'])
def get_qr():
    if request.method == 'POST':
        #receive the json object containing values for generating the qr code
        #json keys are - {vendorid, amount, tokenid(for auth)<ignore for now>}
        pprint(request.json)
        vendorid = request.json['vendorid']
        amount = request.json['amount']
        tokenid = request.json['tokenid']
        url = qr.gen_qr("VID"+vendorid+"AMNT"+amount+"TID"+tokenid)
        url.svg('test.svg', scale = 1 )
        print(url.terminal())
        return qr.qrencode64(url)

#start server if called directly ---> debug mode is on for now

@app.route('/api/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        pprint(request.json)
        username = request.json['username']
        password = request.json['password']

        records= dbcon.query_db("select * from LDAP where EMAIL = ? AND PWD_HASH = ?",  [username, password] , one=True)

        if records is None :
            print("+++++++++++ INVALID CREDENTIALS +++++++++++\n")
            return "+++++++++++ INVALID CREDENTIALS +++++++++++"

        else:

            #if IS_ACTIVE = 1 then auth token is already set, hence return that auth token
            if records["is_active"] == 1:
                return records["current_token"]
            else:

                print("Generating New Token For User")

                #generate new token
                auth_token = secrets.token_hex(32)
                update_query = "UPDATE LDAP SET CURRENT_TOKEN = ?, IS_ACTIVE = 1  WHERE EMAIL = ? "
            
                dbcon.query_db(update_query, [auth_token, username], one=True)
                return auth_token
    else:
        return "+++++++++++ INVALID REQUEST METHOD ++++++++++++++"



@app.route('/api/check_balance', methods = ['POST'])
@login_required
def check_balance():
    pprint(request.json)
    auth_token = request.json['auth_token']
    query = "select * from LDAP where CURRENT_TOKEN = ?"
    records = dbcon.query_db(query, [auth_token], one=True)
    print("Current Balance: {}".format(records["balance"]))
    return str(records["balance"])



@app.route('/api/p2p', methods=['POST'])
@login_required
def p2p():
    pprint(request.json)
    auth_token = request.json["auth_token"]
    query = 'select * from LDAP where CURRENT_TOKEN = ?'
    payer_records = dbcon.query_db(query, [auth_token], one=True)
    payer = payer_records["email"]
    payee = request.json["payee"]
    tx_amount = int(request.json["amount"])

    #check validity of payee
    payee_records = dbcon.query_db("select * from LDAP where EMAIL = ?", [payee], one=True)
    if payee_records is None:
        print("+++++++++++ PAYEE DOES NOT EXIST +++++++++++\n")
        return "+++++++++++ PAYEE DOES NOT EXIST +++++++++++"
    
    #checking if payer has enough balance

    if payer_records["balance"] >= tx_amount :
        #update payee and payer records
        dbcon.query_db("update LDAP set BALANCE = ? where EMAIL = ? ", [payee_records["balance"] + tx_amount, payee], one=True)
        dbcon.query_db("update LDAP set BALANCE = ? where EMAIL = ?", [payer_records["balance"] - tx_amount, payer], one=True)
            
        print("SUCCESS\n")
        return "TX SUCCESS"

    else:
        print("+++++++++++ BALANCE UNDERFLOW +++++++++++\n")
        return "+++++++++++ BALANCE UNDERFLOW +++++++++++"

        




@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database' , None)
    if db is not None:
        db.close()



if __name__ == '__main__':
    app.run(debug = True)
    #app.run(host='0.0.0.0')


