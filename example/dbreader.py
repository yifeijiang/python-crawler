import bsddb     # python-bsddb3 #http://pybsddb.sourceforge.net/bsddb3.html  #
import sys 
class DBReader(object):
    def __init__(self, db_file):
        self.database_file = db_file
        self.database = bsddb.db.DB(None,0)
        self.database.open(self.database_file,dbname=None,mode=0,txn=None)
        
    def close(self):
        self.database.close()

    def get_cursor(self):
        return self.database.cursor()
        
if __name__ == "__main__":
    
    
                    
    dbfile = str(sys.argv[1])
    db_rec_start = int(sys.argv[2])
    db_rec_end = int(sys.argv[3])
    
    db =  DBReader(dbfile)

    try:
        db_cursor = db.get_cursor()
        flag = ""
        cnt = 0
        while flag !=None:
            cnt += 1
            flag = db_cursor.next()
            if flag != None and cnt >= db_rec_start and cnt <= db_rec_end:
                print "######### KEY ###########",flag[0]
                f = open(flag[0].split("?id=")[1]+".html", 'w')
                f.write(flag[1])
                f.close()
                #print "@@@@@@@@@ VALUE @@@@@@@@@",flag[1]
            if cnt > db_rec_end:
                break
    finally:
        db_cursor.close()
        db.close()

