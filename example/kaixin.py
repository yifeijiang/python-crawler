# program requirement 
# python 2.7        http://www.python.org/download/releases/2.7/
# python-crawler       http://pypi.python.org/pypi/crawler/0.1.0
# python-lxml      http://pypi.python.org/pypi/lxml/2.3beta1

import time
from crawler.downloader import DownloadManager# python-crawler
from crawler.webpage import WebPage  # python-crawler
import lxml.html    # python-lxml

import json
import time
import random
import re
import sys
downloader = DownloadManager()
item_prices = {}

def login(user, pwd):

    url = "http://kaixin001.com/"
    error_msg, url, redirected_url, html = downloader.download(url)
    #print error_msg, url, redirected_url, len(html)
    time.sleep(2)


    page = WebPage(url, html)
    action, fields = page.get_form(0)
    fields['email'] = user
    fields['password'] = pwd
    fields['remember'] = 0

    url = 'http://www.kaixin001.com/login/login.php'
    error_msg, url, redirected_url, html = downloader.download(url , fields)
    print error_msg, url, redirected_url, len(html)
    time.sleep(2)
    if redirected_url.count('?uid=') >0:
        return True
    else:
        return False


def get_buy_info():
    url = 'http://www.kaixin001.com/!stall/!ajax/storegoods.php'
    #
    error_msg, url, redirected_url, html = downloader.download(url)
    sales = json.loads(html)
    return sales['goods']['goodsid'],sales['goods']['price'], sales['goods']['salenum']

def sell(goodsid, num):
    url = "http://www.kaixin001.com/!stall/!dialog/salestoregoods.php"
    error_msg, url, redirected_url, html = downloader.download(url)
    #print error_msg, url, redirected_url, len(html)
    page = WebPage(url, html)

    # find buy num
    ele = page.doc.get_element_by_id('saleGoods'+goodsid)
    ele2 = ele.find_class("c9 ffc tac")
    raw =  ele2[0].text_content()
    want = re.search(re.compile('[0-9]+'),raw)
    wants =  want.group(0)
    
    if int(wants) == 0:
        return False    
    # prepare request data
    url, data = page.get_form(0)
    ndata = {}
    ndata['stallid'] = data['stallid']
    ndata['goodsid'] = goodsid

    if int(num) > int(wants):
        ndata['num'] = str(wants)
    else:
        ndata['num'] = str(num)

    #submit sell request
    error_msg, url, redirected_url, html = downloader.download(url, ndata)
    print "start selling....", time.ctime()
    return True

    
def check_price():
    global item_prices
    url =  "http://www.kaixin001.com/!stall/!dialog/buygoodsfromsys.php"
    error_msg, url, redirected_url, html = downloader.download(url)
    page = WebPage(url, html)

    print page.doc.items()

    ele = page.doc.findall('.//li')
    for e in ele:
        #print lxml.html.tostring(e)
        classes = e.find_class('name')
        name = classes[0].text_content()


        price = e.find_class('price')
        a = price[0].find('.//span')
        price =   a.text_content()

        #print name, price
        if name in item_prices:
            if price not in item_prices[name]:
                item_prices[name].append(price)
        else:
                item_prices[name] = [price]
    f =open('price.dat','w')
    st = json.dumps(item_prices)
    f.write(st)
    f.close()


if __name__== "__main__":
    user = sys.argv[1]
    pwd = sys.argv[2]
    while 1:
        ret = login(user, pwd)
        if ret == True:
            print "login into system"
            break
        else:
            print "login failed, sleep 10 second"
            time.sleep(10)


    while 1:
        gid, price, num = get_buy_info()
        if price > 0 :
            sell(gid, num)
            
        s = random.randint(5,10)*60
        time.sleep(s)

