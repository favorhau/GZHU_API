from rsa import rsa_enc, rsa_dec
import requests
import re


class Account(object):
    """Account
    """
    def __init__(self, usn, pwd) -> None:
        """
        :param usn: str, the username of account
        :param pwd: str, the password of account
        """
        self.usn = usn
        self.pwd = pwd
        self.is_login = False
        self.stu_name = None
        self.session = requests.session()
        
    def _login_url(self) -> str:
        return "https://newcas.gzhu.edu.cn/cas/login?"
        
    def login(self) -> bool:
        """
        Auth to GZHU website
        """
        url = self._login_url()
        self.session.cookies.clear()
        get_res = self.session.get(url, verify=True)
        lt = re.findall(r'name="lt" value="(.*)"', get_res.text)
        login_form = {
        'username': self.usn,
        'password': self.pwd,
        'ul': len(self.usn),
        'pl': len(self.pwd),
        'lt': lt[0],
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rsa': rsa_enc(self.usn + self.pwd + lt[0])
        }
        post_res = self.session.post(url, data=login_form)
        if self.usn in post_res.text:
            return True
        else:
            return False
        

