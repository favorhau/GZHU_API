# index.py
# version: 1.0

import re
from utils import Account
from flask import Flask, request
import redis
import hashlib
import time

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
    if not _token:
        if 'auth' in request.url:
            pass
        else:
            res["msg"] = "Token needed"
            return res
    else:
        res_token = r.get(_token)
        if res_token:
            pass
        else:
            res["msg"] = "Invaild token"
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
            token = hashlib.new('md5', "*1%.2{}3e822121{}".format(_username, time.time()).encode("utf-8")).hexdigest()
            res["msg"] = "login success"
            res["token"] = token
            r.set(token, _username, ex=1296000)
            accounts[_username] = account
        else:
            res["msg"] = "username or password is wrong"
    except Exception as e:
        res["msg"] = "Unkown exception"
    
    return res

@app.route("/v1/info", methods=['POST'])
def info():
    _token = request.headers.get('token')
    _username = r.get(_token)
    print(_username)
app.run()