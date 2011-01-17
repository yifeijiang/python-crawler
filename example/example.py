from crawler.crawler import Crawler

mycrawler = Crawler()

seeds = ['http://www.example.com/'] # list of url

mycrawler.add_seeds(seeds)

url_patterns = ['^(.+example\.com)(.+)$'] # list of regular expression for urls that crawler will work on.

mycrawler.start(url_patterns) # start crawling
