import redis, time

from redis.client import Pipeline

ts = time.time()
#rclient = redis.Redis(decode_responses=True)
rclient = redis.Redis('192.168.1.65',10025,decode_responses=True)
#rclient = redis.Redis('testzs.centralus.redisenterprise.cache.azure.net',10000,0,'IjzpYma0DhvcOORzIBqMWz4MIuz8WGE3vTZCi0PPYJk=',decode_responses=True)

cnt=0

p = rclient.pipeline()
p.multi()
        
for x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    for y in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        for z in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            cnt = cnt+1
            mapping = {(z+y+x):cnt}
            p.zadd('myvset',mapping)
p.execute()

mapping = {'ts':ts}
answer = rclient.zadd('myvset',mapping)   
print(answer)

p = rclient.pipeline()
p.multi()
for x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    for y in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        for z in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            mapping = {(z+y+x):0}
            p.zadd('myset',mapping)
p.execute()

mapping = {'ts':ts}
answer = rclient.zadd('myset',mapping)   
print(answer)

answer = rclient.zlexcount('myset', '-', '+')
print('Length of myset = '+str(answer))
answer = rclient.zlexcount('myvset', '-', '+')
print('Length of myvset = '+str(answer))

