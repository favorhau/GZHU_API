# index.py
# version: 1.0

from typing import Dict

from flask.globals import session
from utils import Account
from flask import Flask, request
import redis
import hashlib
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379)
accounts : Dict[str, Account] = {}

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
            res["msg"] = "Invalid token"
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
        res["msg"] = "Catch exception: {}".format(e)

    return res

@app.route("/v1/info", methods=['POST'])
def info():
    """
    Get the students info
    """
    _token = request.headers.get('token')
    _username = r.get(_token).decode("utf-8")
    res = {
    "msg": None,
    "data": {}
    }
    
    try:
        account = accounts[_username]
        PIThree = account.get_stu_info(1)
        NetFee = account.get_stu_info(2)
        ECard = account.get_stu_info(3)
        res["msg"] = "success"
        res['data']['PIThree'] = PIThree
        res['data']['NetFee'] = NetFee
        res['data']['ECard'] = ECard
        
    except Exception as e:
        res["msg"] = "Catch exception: {}".format(str(e))
        
    return res
    
    
@app.route("/v1/trans", methods=['POST'])
def trans():
    """
    Get the students Transcript
    """
    _data = eval(request.data)
    _token = request.headers.get('token')
    _username = r.get(_token).decode("utf-8")
    _year = _data['year']
    _term = _data['term']
    
    res = {
    "msg": None,
    "data": {}
    }
    try:
        account = accounts[_username]
        res["msg"] = "success"
        res['data'] = account.get_stu_trans(year=_year, term=eval(_term))
        
    except Exception as e:
        res["msg"] = "Catch exception: {}".format(str(e))
        
    return res
    

app.run('0.0.0.0', port=8080)