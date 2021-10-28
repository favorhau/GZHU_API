from re import A
import redis

r = redis.Redis(host='localhost', port=6379)
a= r.set('python', '1')
print(a)