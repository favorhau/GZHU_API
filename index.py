import json
from utils import Account
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    account = Account('2006100062', '257314')
    return json.dumps(account.get_stu_credit())
    