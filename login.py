from flask import request, Flask
from pprint import pprint
import dbcon

# If a person is logged in => auth_token is set and he passes it in the request
# Therefore only auth token check is required
# If auth_token exists in DB means that user is authenticated

def login_required(func):
    def wrapper():
        if request.method == 'POST':
            print("Decorator Check\n")
            pprint(request.json)
            auth_token = request.json['auth_token']

            records = dbcon.query_db("select * from LDAP where CURRENT_TOKEN = ? AND IS_ACTIVE = 1", [auth_token], one=True)
            
            if records is None:
                return "+++++++++++ AUTH FAiLURE +++++++++++" 
            else:
                return func()
    #renaming name of wrapper to function name
    wrapper.__name__ = func.__name__
    return wrapper



            

