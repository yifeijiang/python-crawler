import os
from crawler.crawler import Crawler


mycrawler = Crawler()
seeds = ['http://www.example.com/'] # list of url
mycrawler.add_seeds(seeds)
rules = {'^(http://.+example\.com)(.+)$':[ '^(http://.+example\.com)(.+)$' ]}
#your crawling rules: a dictionary type, 
#key is the regular expressions for url, 
#value is the list of regular expressions for urls which you want to follow from the url in key.
mycrawler.add_rules(rules)
mycrawler.start() # start crawling
