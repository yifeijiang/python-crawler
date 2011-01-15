import bsddb     # python-bsddb3
class CrawlerDB:
    pass

class QueueDB( CrawlerDB ):
    pass

class WebpageDB( CrawlerDB ):
    pass

class DuplCheckDB( CrawlerDB ):
    pass

class MySqlDB:
    pass

class BerkeleyDB:
    pass

class bdb:
    "PACKAGE FOR BERKERLY DB "

    def __init__(self,file,type=None,cache=False,readonly=False):
        self.BDB = bsddb.db.DB(None,0)
        
        if readonly == True:
            self.BDB.open(file,dbname=None,mode=0,txn=None)
            return
        if type == 'DB_HASH':
            if cache == True:
                self.BDB.set_cachesize(0,536870912)
            self.BDB.open(file,dbname=None,dbtype=bsddb.db.DB_HASH,flags=bsddb.db.DB_CREATE,mode=0,txn=None)
        elif type == 'DB_BTREE':
            if cache == True:
                self.BDB.set_cachesize(0,536870912)
            self.BDB.open(file,dbname=None,dbtype=bsddb.db.DB_BTREE,flags=bsddb.db.DB_CREATE,mode=0,txn=None)
        elif type == 'DB_QUEUE':
            self.BDB.set_re_len(256)
            self.BDB.open(file,dbname=None,dbtype=bsddb.db.DB_QUEUE,flags=bsddb.db.DB_CREATE,mode=0,txn=None)
        elif type == 'DB_RECNO':
            self.BDB.open(file,dbname=None,dbtype=bsddb.db.DB_RECNO,flags=bsddb.db.DB_CREATE,mode=0,txn=None)
        else:
            self.BDB.open(file,dbname=None,mode=0,txn=None)
            
    
        
    def close(self):
        self.BDB.close()

    def dup_check(self,keylis):
        newlis = []
        for key in keylis:
            key = str(key)
            if self.BDB.get(key)==None:
                newlis.append(key)
        return newlis


    def get_cursor(self):
        return self.BDB.cursor()

    
    def add(self,key,val):
        try:
            self.BDB.put(key,val)
        except:
            print len(key)
            print len(val)
            raise
    def put(self,key,val):
        try:
            self.BDB.put(key,val)
        except:
            print len(key)
            print len(val)
            raise


    def increase(self,key,num):
        sval = self.BDB.get(key)
        if sval==None:
            self.BDB.put(key,"1")
            return 1
        else:
            val = int(sval.strip())
            self.BDB.put(key,str(val+1))
            return val+1

    def get(self,key):
        sval = self.BDB.get(key)
        return sval
    
    def exist(self,key):
        sval = self.BDB.get(key)
        if sval != None:
            return True
        else:
            return False

class bdb_queue(bdb):
    def __init__(self,file,length):
        self.BDB = bsddb.db.DB(None,0)
        self.BDB.set_re_len(length)
        self.BDB.open(file,dbname=None,dbtype=bsddb.db.DB_QUEUE,flags=bsddb.db.DB_CREATE,mode=0,txn=None)

    def pop(self):
        return self.BDB.consume()

    def consume(self):
        return self.BDB.consume()

    def add_list(self,keylis):
        for key in keylis:
            self.BDB.append(key)
    def append(self,key):
        self.BDB.append(key)

class bdb_hash(bdb):
    def __init__(self,file):
        self.BDB = bsddb.db.DB(None,0)
        self.BDB.open(file,dbname=None,dbtype=bsddb.db.DB_HASH,flags=bsddb.db.DB_CREATE,mode=0,txn=None)
    
    def add_list(self,keylis):
        for key in keylis:
            self.BDB.put(key,'')    

##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################

#import MySQLdb

class Jmysql:
    
    def __init__(self,phost,puser,ppwd,pdb):
        self.db = MySQLdb.connect(host = phost,user = puser, passwd = ppwd, db = pdb)
        self.cr = self.db.cursor()
    
    def execute(self,SQL):
        self.cr.execute(SQL)
    
    def isDataExist(self,SQL):
        self.cr.execute(SQL)
        numrows = int(self.cr.rowcount)
        if numrows >0:
            return True
        else:
            return False
    def select(self,SQL):
        self.cr.execute(SQL)
        numrow = int(self.cr.rowcount)
        return self.cr.fetchall()
