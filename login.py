from flask import request, Flask
from pprint import pprint
import dbcon

# If a person is logged in => auth_token is set and he passes it in the request
# Therefore only auth token check is required
# If auth_token exists in DB means that user is authenticated

def login_required(func):
    def wrapper():
        if request.method == 'POST':
            pprint(request.json)
            username = request.json['username']
            password = request.json['password']
            auth_token = request.json['auth_token']

            records = dbcon.query_db("select * from LDAP where EMAIL = ? AND PWD_HASH = ? AND CURRENT_TOKEN = ? AND IS_ACTIVE = 1", [username, password, auth_token], one=True)
            #print(records)
            #print("==================")
            if records is None:
                return "Invalid Record" 
            else:
                func()
                return func()
    return wrapper



            

