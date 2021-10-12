from .rsa import rsa_enc, rsa_dec
import requests
import re
import json


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
        
    def _get_login_url(self) -> str:
        return "https://newcas.gzhu.edu.cn/cas/login?"
        
    def _get_stu_info_url(self) -> str:
        return "https://newmy.gzhu.edu.cn/up/up/gzhuStaffInfo/{}"
        
    def login(self) -> bool:
        """
        Auth to GZHU website
        :return: bool, login result for success or error
        """
        url = self._get_login_url()
        self.session.cookies.clear()
        get_res = self.session.get(url, verify=True, timeout=5)
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
        post_res = self.session.post(url, data=login_form,timeout=5)
        if self.usn in post_res.text:
            self.is_login = True
            return True
        else:
            return False
            
    def get_stu_info(self, type = 1) -> str:
        """
        Get specific infomation of student
        :param type: int, option:1,2 and 3, 1 is personal info, 2 is netfee info, 3 is ecard info. defalt: 1
        :return type: object, infomation for user
        """
        if self.is_login:
            url = self._get_stu_info_url()
            if type == 1:
                post_res = self.session.post(url.format('getPIThree'), verify=True,timeout=5)
            elif type == 2:
                post_res = self.session.post(url.format('getNetFee'), verify=True,timeout=5)
            else:
                post_res = self.session.post(url.format('getECard'), verify=True,timeout=5)
            
            try:
                res = json.loads(post_res.text)
            except Exception:
                res = {}
                
            return res
        else:
            raise Exception('Login is needed')

