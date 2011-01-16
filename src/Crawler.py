import sys
import re
import time

SOCKET_DEFAULT_TIMEOUT = 10

class crawler():

    def __init__(self ):
        #self.seeds = seeds
        self.download_error = 0    
        self.cookie = None    
        ######
        #self.db_html = None
        #self.db_queue = None
        #self.db_seenurls = None
        ######

    def add_seeds(self, seeds):
        self.seeds.extend(seeds)

    def seed2db(self, seed, db_queue, db_seen):
        url = seed
        sval = db_seen.get(url)
        if sval==None:
            db_queue.append(url)
            db_seen.put(url,"")
        #self.seeds = []

    def pop_url(self, qdb):
        item = qdb.consume()
        if item == None:
            return None
        return item[1].strip()

    """    
    def open_htmldb(self, dbname):
        bdb = bsddb.db.DB(None,0)
        bdb.set_cachesize(0,536870912)
        bdb.open(dbname, dbname=None, dbtype=bsddb.db.DB_HASH, flags=bsddb.db.DB_CREATE, mode=0, txn=None)
        self.db_html = bdb

    def open_queuedb(self, dbname):
        bdb = bsddb.db.DB(None,0)
        bdb.set_re_len(1024)
        bdb.open(dbname, dbname=None, dbtype=bsddb.db.DB_QUEUE, flags=bsddb.db.DB_CREATE, mode=0, txn=None)
        self.db_queue = bdb

    def open_seenurlsdb(self, dbname):
        bdb = bsddb.db.DB(None,0)
        bdb.set_cachesize(0,536870912)
        bdb.open(dbname, dbname=None, dbtype=bsddb.db.DB_HASH, flags=bsddb.db.DB_CREATE, mode=0, txn=None)
        self.db_seenurls = bdb
    """


    def addurlseen(self, link, dbseen):
        pass

    
    def pushlink(self, link, queuedb, seendb, ):
        sval = seendb.get(link)
        if sval==None:
            seendb.put(link,"")
            queuedb.append(link)

    def html2bdb(self,url, htmlcode, htmldb):
        htmldb.put(url,htmlcode)

       
    def mysleep(self, n):
        for i in range(n):
            time.sleep(1)
            print "sleep",i,"of",n

    #####################################
    def is_exsit(self, value, db):

        sval = db.get(value)
        if sval==None:
            return False
        else:
            return True


if __name__ == "__main__":
    pass
