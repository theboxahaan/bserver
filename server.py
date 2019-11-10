from flask import Flask
from flask import request, jsonify, make_response, g
from pprint import pprint
import qr
import dbcon
from werkzeug.datastructures import MultiDict
import os, sys
import secrets

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
        # connector = dbcon.get_db()
        records= dbcon.query_db("select * from LDAP where EMAIL = ? AND PWD_HASH = ? AND CURRENT_TOKEN = '0' ",  [username, password] , one=True)
        if records is None :
            print("Error Code is - Can be Anything MoFo\n")
            return "MOFO"
        else: 
            print("Current Token is: " + records["current_token"] + '\n')
            #generate new token
            auth_token = secrets.token_hex(32)
            update_query = "UPDATE LDAP SET CURRENT_TOKEN = ? WHERE EMAIL = ? "
            dbcon.query_db(update_query, ["0", username], one=True)
            return auth_token     


        


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database' , None)
    if db is not None:
        db.close()



if __name__ == '__main__':
    app.run(debug = True)
    #app.run(host='0.0.0.0')


