import sys
from crawler.database import WebpageDB
kaixindb =  WebpageDB('stall.db')


rec_num = int(sys.argv[1])


try:
    DBCursor = kaixindb.get_cursor()
    print "a"
    flag = ""
    cnt = 0
    while flag !=None:
        cnt += 1
        flag =  DBCursor.next()
        if flag != None: #and cnt == rec_num:
            print "######### KEY ###########",flag[0]
            print "@@@@@@@@@ VALUE @@@@@@@@@",flag[1]
            #break
finally:
    DBCursor.close()
    kaixindb.close()

