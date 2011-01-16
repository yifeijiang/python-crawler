import sys
import re
import time
from crawler_database import QueueDB, WebpageDB, DuplCheckDB
from download_manager import DownloadManager
from webpage import WebPage

class Crawler():

    def __init__(self ):
        self.downloader = DownloadManager()
        self.webpage = None
        self.init_database()

    def init_database(self):
        self.queue = QueueDB('queue.db')
        self.webpage = WebpageDB('webpage.db')
        self.duplcheck = DuplCheckDB('duplcheck.db')
    
    def add_seeds(self, links):
        new_links = self.duplcheck.filter_dupl_urls(links)
        self.duplcheck.add_urls(new_links)
        self.queue.push_urls(new_links)
            
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
                self.webpage = WebPage(url,html)
                self.webpage.parse_links()
                links = self.webpage.filter_links(tags = ['a'], str_patterns= ['^(http://.+livejournal\.com)(.+)$'])
                self.add_seeds(links)
            self.mysleep(3)        

    def mysleep(self, n):
        for i in range(n):
            time.sleep(1)
            print "sleep",i,"of",n



if __name__ == "__main__":
    mycrawler = Crawler()
    mycrawler.add_seeds(['http://www.livejournal.com/'])
    mycrawler.start()
