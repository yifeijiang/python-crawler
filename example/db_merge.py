import sys
from crawler.database import WebpageDB
import json
kaixindb =  WebpageDB('stall.db')
kaixindb2 =  WebpageDB('stall2.db')

prices = {}
try:
    DBCursor = kaixindb2.get_cursor()
    flag = ""
    cnt = 0
    while flag !=None:
        cnt += 1
        flag =  DBCursor.next()
        if flag != None :
            key = str(flag[0])
            val = json.loads(flag[1])
            prices[key] = val 
finally:
    DBCursor.close()
    kaixindb2.close()

try:
    DBCursor = kaixindb.get_cursor()
    flag = ""
    cnt = 0
    while flag !=None:
        cnt += 1
        flag =  DBCursor.next()
        if flag != None :
            key = str(flag[0])
            val = json.loads(flag[1])
            if key in prices:
                prices[key] = sorted( list( set( prices[key] )|set( val ) ) )
            else:
                prices[key] = val 
finally:
    DBCursor.close()
    kaixindb.close()


try:
    kaixindb =  WebpageDB('stall_all.db')
    for k, v in prices.items():
        print k,v
        kaixindb.insert( k, json.dumps( v ) )
finally:
    kaixindb.close()
    
