# otPerfTestSortedSet
The two files in this project are used to test the performance of executing many calls to ZLEXCOUNT against SortedSets in Redis.

The question being answered is:  Does it matter if the SortedSet Score values are all the same (zeroed out)?
The API call ZLEXCOUNT is the only one tested in this code (as of June 17th 2021)

TestSortedSetBehavior.py Loads the two sortedSets with data. (each gets 238,329 entries)

The 'myset' SortedSet has all of the scores zeroed out (set to zero 0 )

<code>

192.168.1.65:10025> zlexcount myset - +

(integer) 238329

192.168.1.65:10025> zlexcount myset [aaa [caa

(integer) 7689

192.168.1.65:10025> zrange myset -4 -2  withscores

1) "zzx"
2) "0"
3) "zzy"
4) "0"
5) "zzz"
6) "0"

</code>

The 'myvset' SortedSet has each score set as 1 larger than the one before.  
This makes them all unique and ordered according to score not value.

<code>

192.168.1.65:10025> zlexcount myvset - +

(integer) 238329

192.168.1.65:10025> zlexcount myvset [aaa [caa

(integer) 2

192.168.1.65:10025> zrange myvset -4 -2  withscores

1) "799"
2) "238326"
3) "899"
4) "238327"
5) "999"
6) "238328"

</code>
