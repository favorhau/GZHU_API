from re import A
import redis
import time
r = redis.Redis(host='localhost', port=6379)
a= r.set('python', '1' , ex=1)
print(r.get('python'))
time.sleep(1)
print(r.get('python'))
