# python crawler spider #
# Web Crawler #
### Example Code ###
```
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
```

### data files ###
three database (Berkeley DB) files will be generated.
  * queue.db
  * webpage.db
  * duplcheck.db

### windows installation howto: ###
  * STEP1 - download and install python 2.7 http://www.python.org/download/releases/2.7/
  * STEP2 - download and install python-lxml http://pypi.python.org/pypi/lxml/2.3beta1
  * STEP3 - install python-crawler http://pypi.python.org/pypi/crawler/0.1.2


### ubuntu installation howto: ###

  * apt-get install python-lxml
  * apt-get install python-bsddb3
  * install python-crawler : python setup.py install
