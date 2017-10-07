import redis

r = redis.Redis(host= 'localhost', port = 6379, db = 1)
r.set ('k1',  'v1')
r.set('k2', 'v2')
print (r.get('v1'))
print (r.keys())
print (r.dbsize())
r.delete('k2')
print (r.dbsize())

p = r.pipeline()
p.set('k3', 'v4')
p.set('k4', 'v4')
p.incr('num')
p.incr('num')
p.execute()
print (r.get('num'))
