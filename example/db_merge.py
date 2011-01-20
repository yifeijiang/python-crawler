import sys
from crawler.database import WebpageDB
import json
kaixindb =  WebpageDB('stall.db')
kaixindb2 =  WebpageDB('stall_xin.db')



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
            print key,val
            
finally:
    DBCursor.close()
    kaixindb.close()
    kaixindb2.close()
