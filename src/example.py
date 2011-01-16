from crawler import Crawler

mycrawler = Crawler()
mycrawler.add_seeds(['http://www.livejournal.com/'])
mycrawler.start(['^(http://.+livejournal\.com)(.+)$'])
