import re, sys
import pycrawlerlib


db_html = "./html.db"
db_queue = "./queue.db"
db_seenurls = "./seenurls.db"

mycrawler = pycrawlerlib.crawler(["http://www.livejournal.com"])
mycrawler.open_htmldb(db_html)
mycrawler.open_queuedb(db_queue)
mycrawler.open_seenurlsdb(db_seenurls)
mycrawler.set_cookie_redirect()
mycrawler.set_socket_timeout()

mycrawler.seeds2db()

while True:
	url = mycrawler.pop_url(mycrawler.db_queue)
	print url
	if url == None:
		break
	html = pycrawlerlib.htmlpage(url)
	html.fetch()
	html.parse_links()
	html.filter_links([],[re.compile("^(http://)(.)+livejournal\.com.+")])
	html.html2bdb( mycrawler.db_html )
	html.links2bdb( mycrawler.db_seenurls, mycrawler.db_queue )

