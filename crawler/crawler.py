import sys
import re
import time
from database import QueueDB, WebpageDB, DuplCheckDB
from downloader import DownloadManager
from webpage import WebPage

class Crawler(object):

    def __init__(self ):
        super(Crawler, self).__init__()
        self.downloader = DownloadManager()
        self.webpage = None
        self.init_database()
        self.rules = {}

    def init_database(self):
        self.queue = QueueDB('queue.db')
        self.webpagedb = WebpageDB('webpage.db')
        self.duplcheck = DuplCheckDB('duplcheck.db')
    
    def add_seeds(self, links):
        new_links = self.duplcheck.filter_dupl_urls(links)
        self.duplcheck.add_urls(new_links)
        self.queue.push_urls(new_links)
    
    def add_rules(self, rules):
        self.rules = {}
        for url, inurls in rules.items():
            reurl = re.compile(url)
            repatn = []
            for u in inurls:
                repatn.append(re.compile(u))
            self.rules[reurl] = repatn

    def get_patterns_from_rules(self,url):
        patns = []
        for purl,ru in self.rules.items():
            if purl.match(url)!= None:
                patns.extend(ru)
        return list(set(patns))

    def getlinks(self,url,html):
        self.webpage = WebPage(url,html)
        self.webpage.parse_links()
        ruptn = self.get_patterns_from_rules(url)
        #print ruptn
        links = self.webpage.filter_links(tags = ['a'], patterns= ruptn)
        return links
        
    def start(self):
        while 1:
            url = self.queue.pop_url()
            print url
            if url == None:
                print "crawling task is done."
                break
            error_msg, url, redirected_url, html = self.downloader.download(url)
            #print error_msg, url, redirected_url, html
            if html !=None:
                self.webpagedb.html2db(url,html)
                links = self.getlinks(url, html)
                self.add_seeds(links)
            self.mysleep(3)        

    def mysleep(self, n):
        for i in range(n):
            time.sleep(1)
            print "sleep",i,"of",n



if __name__ == "__main__":
    import json
    if len(sys.argv) < 2:
        print "Input Error: python crawler.py config-file-name"
        sys.exit(0)
    try:
        f = open(sys.argv[1],'r')
    except:
        print "Can't find file: "+ sys.argv[1];
        sys.exit(0)

    mycrawler = Crawler()
    for line in f:
        line = line.replace('\n','')
        if line[0:4] == 'seed':
            dat = line[4:].strip()
            print "add seeds: ", dat
            seed = json.loads(dat)
            #print seed
            mycrawler.add_seeds(seed)
        if line[0:4] == 'rule':
            dat = line[4:].strip()
            print "add rules: ", dat
            rule = json.loads( dat ) 
            #print rule
            mycrawler.add_rules(rule)
            
    mycrawler.start()


