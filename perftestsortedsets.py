import redis, time

rclient = redis.Redis('192.168.1.65',10025,decode_responses=True)
#rclient = redis.Redis('testzs.centralus.redisenterprise.cache.azure.net',10000,0,'IjzpYma0DhvcOORzIBqMWz4MIuz8WGE3vTZCi0PPYJk=',decode_responses=True)
#rclient = redis.Redis(decode_responses=True)

timetotal1 = 0
timetotal2 = 0
numit = 0

for x in "abcdefghijklmnopqrstuvwxy":
    for y in "abcdefghijklmnopqrst":
        p = rclient.pipeline()
        p.multi() 
        ts1 = p.time() # timestamp1
        p.zlexcount('myvset', '[a'+x+y, '[w'+y+x)
        ts2 = p.time()  # timestamp2
        result = p.execute()
        it = iter(result)
        cntr = 0
        for xx in it:
            if cntr == 0:
                (ftf,ftmicro)=xx # this allows the extraction of the two time values
            if cntr == 2:
                (stf,stmicro)=xx # this allows the extraction of the two time values
            cntr = cntr + 1
        if stmicro>ftmicro:
            timetotal2 += stmicro-ftmicro
        if ftmicro > stmicro:
            stmicro = stmicro+1000000
            timetotal2 += stmicro-ftmicro
            #print('sample delta: '+str(stmicro-ftmicro))
        numit = numit +1

print('Testing sortedSet WITH varying scores')
print('executed '+str(numit)+' iterations...')
print('Time taken WITH varying scores: '+str(timetotal2))

numit = 0

for x in "abcdefghijklmnopqrstuvwxy":
    for y in "abcdefghijklmnopqrst":
        p = rclient.pipeline()
        p.multi() 
        ts1 = p.time() # timestamp1
        p.zlexcount('myset', '[a'+x+y, '[w'+y+x)
        ts2 = p.time()  # timestamp2
        result = p.execute()
        it = iter(result)
        cntr = 0
        for xx in it:
            if cntr == 0:
                (ftf,ftmicro)=xx # this allows the extraction of the two time values
            if cntr == 2:
                (stf,stmicro)=xx # this allows the extraction of the two time values
            cntr = cntr + 1
        
        if stmicro>ftmicro: # subtract the smaller microsecond measure from the larger
            timetotal1 += stmicro-ftmicro
        if ftmicro > stmicro: # subtract the smaller microsecond measure from the larger
            stmicro = stmicro+1000000 # the second has flipped over - we need it back 
            timetotal1 += stmicro-ftmicro

        numit = numit +1

print('Testing sortedSet with ZEROED scores')
print('executed '+str(numit)+' iterations...')
print('Time taken ZEROED scores: '+str(timetotal1))


if timetotal1>timetotal2:
    print('delta = '+str(timetotal1-timetotal2)+' or: '+str((timetotal1-timetotal2)/1000000)+' seconds')

if timetotal2>timetotal1:
    print('delta = '+str(timetotal2-timetotal1)+' or: '+str((timetotal2-timetotal1)/1000000)+' seconds')
