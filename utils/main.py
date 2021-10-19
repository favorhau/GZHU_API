from os import EX_OSFILE
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
        self.session = requests.session()
        
    def _get_login_url(self) -> str:
        return "https://newcas.gzhu.edu.cn/cas/login?"
        
    def _get_stu_info_url(self) -> str:
        return "https://newmy.gzhu.edu.cn/up/up/gzhuStaffInfo/{}"
        
    def _get_process_doing(self) -> str:
        return "https://newmy.gzhu.edu.cn/up/up/gzhuStaffInfo/getProcessDoing"
        
    def _get_sso_url(self) -> str:
        return "http://jwxt.gzhu.edu.cn/sso/driot4login"
        
    def _get_stu_trans_url(self) -> str:
        return "http://jwxt.gzhu.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005"
        
    def _get_stu_schedule_url(self) -> str:
        return "http://jwxt.gzhu.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508"
        
    def _get_stu_portrait_url(self) -> str:
        return "http://jwxt.gzhu.edu.cn/jwglxt/xtgl/photo_cxXszp.html?xh_id={}&zplx=rxhzp".format(self.usn)
        
    def _get_stu_exam_url(self) -> str:
        return "http://jwxt.gzhu.edu.cn/jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105"
        
    def _get_stu_credit_url(self) -> str:
        return "http://jwxt.gzhu.edu.cn/jwglxt/xsxy/xsxyqk_cxKczxAllIndex.html?doType=query&gnmkdm=N105515"
        
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
            sso_url = self._get_sso_url()
            self.session.get(sso_url, verify=False, timeout=5)
            self.is_login = True
            return True
        else:
            return False
            
    def get_stu_info(self, type=1) -> dict:
        """
        Get specific infomation of student
        :param type: int, option:1,2 and 3, 1 is personal info, 2 is netfee info, 3 is ecard info. defalt: 1
        :return : dict, infomation for user
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
            
    def get_process_doing(self) -> list:
        """
        Get the student on-going workflow in taskcenter
        :return :list, On-going task in taskcenter
        """
        if self.is_login:
            url = self._get_process_doing()
            res = self.session.post(url=url, timeout=5)
            
            return eval(res.text)
        else:
            raise Exception('Login is needed')

    def get_stu_trans(self, year='2020', term=1) -> dict:
        """
        Get specific transript of student(user score)
        :param year: str ,2020 means 2020-2021 and 2019 means 2019-2020
        :param term: int ,1 for first term, 2 for second term
        :return : dict, Transcript for user in optional params
        """
        if self.is_login:
            trans_url = self._get_stu_trans_url()
            post_data = {
                'xnm': year,
                'xqm': '3' if term == 1 else '12',
                'queryModel.showCount': '70'
            }
            post_res = self.session.post(url=trans_url, data=post_data, timeout=5)
            try:
                res = json.loads(post_res.text)
            except Exception:
                res = {}
                
            return res
            
        else:
            raise Exception('Login is needed')
            
    def get_stu_gpa(self, year='2020', term=1, all=False) -> float:
        """
        Get specific schedule of student(user score)
        :param year: str ,2020 means 2020-2021 and 2019 means 2019-2020
        :param term: int ,1 for first term, 2 for second term
        :param all: bool,True for all terms gpa, and False for specific term gpa.
        :return : float, GPA(Grade Point Average) for student
        """
        
        if self.is_login:
            url = self._get_stu_trans_url()
            post_data = {
                'xnm': year,
                'xqm': '3' if term == 1 else '12',
                'queryModel.showCount': '70'
            }
            if all:
                post_data['xnm'] = ''
                post_data['xqm'] = ''
            post_res = self.session.post(url=url, data=post_data, timeout=5)
            
            try:
                score = json.loads(post_res.text)
                term_gpas = [float(items['xfjd']) for items in score['items']]
                term_xf = [float(items['xf']) for items in score['items']]
                
                term_gpa = round(sum(term_gpas)/sum(term_xf), 2)
                return term_gpa
                
            except Exception:
                return None
                
        else:
            raise Exception('Login is needed')
        
    def get_stu_schedule(self, year='2021', term=1) -> dict:
        """
        Get Grade Point Average of student(user score)
        :param year: str ,2020 means 2020-2021 and 2019 means 2019-2020
        :param term: int ,1 for first term, 2 for second term
        :return : dict, Schedule for user in optional params
        """
        if self.is_login:
            schedule_url = self._get_stu_schedule_url()
            post_data = {
                'xnm': year,
                'xqm': '3' if term == 1 else '12',
                'queryModel.showCount': '70'
            }
            post_res = self.session.post(url=schedule_url, data=post_data, timeout=5)
            try:
                res = json.loads(post_res.text)
            except Exception:
                res = {}
                
            return res
        else:
            raise Exception('Login is needed')
            
    def get_stu_portrait(self) -> bytes:
        """
        Get the portrait of student
        :return bytes
        """
        if self.is_login:
            url = self._get_stu_portrait_url()
            get_res = self.session.get(url=url, timeout=5)
            return get_res.content
        else:
            raise Exception('Login is needed')
            
    def get_stu_exam(self, year='2021', term=1) -> dict:
        """
        Get Exam infomation for student
        :param year: str ,2020 means 2020-2021 and 2019 means 2019-2020
        :param term: int ,1 for first term, 2 for second term
        :return : dict, Exam information for user in optional params
        """
        if self.is_login:
            exam_url = self._get_stu_exam_url()
            post_data = {
                'xnm': year,
                'xqm': '3' if term == 1 else '12',
                'queryModel.showCount': '70'
            }
            post_res = self.session.post(url=exam_url, data=post_data, timeout=5)
            try:
                res = json.loads(post_res.text)
            except Exception:
                res = {}
                
            return res
        else:
            raise Exception('Login is needed')
            
    def get_stu_credit(self) -> dict:
        """
        Get course study infomation for student
        :return : dict,Get course study details with credit had gotton
        """
        if self.is_login:
            url = self._get_stu_credit_url()
            post_res = self.session.get(url=url, timeout=5)
            try:
                res = json.loads(post_res.text)
            except Exception:
                res = {}
            
            return res
        else:
            raise Exception('Login is needed')