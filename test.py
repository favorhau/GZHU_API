# from re import A, X
# import redis
# import time
# r = redis.Redis(host='localhost', port=6379)
# a= r.set('python', '1' , ex=1)
# print(r.get('python'))
# time.sleep(1)
# print(r.get('python'))

import requests
import urllib3

urllib3.disable_warnings()

res = requests.post("https://newcas.gzhu.edu.cn/cas/login?service=https%3A%2F%2Fnewmy.gzhu.edu.cn%2Fup%2F", verify=False)
print(res.text)