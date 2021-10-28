from utils import Account
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    account = Account('2006100062', '257314')
    account.login()
    return account.get_stu_info()
    