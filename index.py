# index.py
# version: 1.0

import re
import jwt
from utils import Account
from flask import Flask, request
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379)
accounts = {}

@app.before_request
def verify():
    """
    Verify the token of API use
    """
    _token = request.headers.get('token')
    res = {
    "msg": None,
    "data": []
    }
    if not _token and 'verify' not in request.base_url:
        res["msg"] = "Token needed"
    else:
        res_token = r.get(_token)
        if res_token:
            pass
        else:
            res["msg"] = "Token invail"
            
    return res
        
@app.route("/v1/auth", methods=["POST"])
def auth():
    """
    Get the auth Token for API user to verify
    """
    _token = request.headers.get('token')
    _data = eval(request.data)
    res = {
    "msg": None,
    "data": {}
    }
    try:
        if "username" in _data and "password" in _data:
            pass
        _username = _data["username"]
        _password = _data["password"]
        account = Account(_username, _password)
        if account.login():
            res["msg"] = "success"
            res["token"] = 
            accounts[_username] = account
        else:
            res["msg"] = "username or password is wrong"
            
    except Exception:
        res["msg"] = "Unkown exception"
    
    return res

app.run()