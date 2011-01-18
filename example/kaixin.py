# program requirement 
# python 2.7        http://www.python.org/download/releases/2.7/
# python-crawler       http://pypi.python.org/pypi/crawler/0.1.0
# python-lxml      http://pypi.python.org/pypi/lxml/2.3beta1

import time
from crawler.downloader import DownloadManager# python-crawler
from crawler.webpage import WebPage  # python-crawler
from crawler.database import WebpageDB

import lxml.html    # python-lxml

import json
import time
import random
import re
import sys
import json
downloader = DownloadManager()
item_prices = {}
kaixindb =  WebpageDB('stall.db')


def login(user, pwd):

    url = "http://kaixin001.com/"
    error_msg, url, redirected_url, html = download(url)

    page = WebPage(url, html)
    action, fields = page.get_form(0)
    fields['email'] = user
    fields['password'] = pwd
    fields['remember'] = 0

    url = 'http://www.kaixin001.com/login/login.php'
    error_msg, url, redirected_url, html = download(url , fields)
    #print error_msg, url, redirected_url, len(html)
    if redirected_url.count('?uid=') >0:
        return True
    else:
        return False


def get_buy_info():
    url = 'http://www.kaixin001.com/!stall/!ajax/storegoods.php'
    #
    error_msg, url, redirected_url, html = download(url)

    sales = json.loads(html)
    return sales['goods']['goodsid'],sales['goods']['price'], sales['goods']['salenum']

def sell(goodsid, num):
    url = "http://www.kaixin001.com/!stall/!dialog/salestoregoods.php"
    error_msg, url, redirected_url, html = download(url)

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
    error_msg, url, redirected_url, html = download(url, ndata)
    #print "start selling....", time.ctime()
    return True

#######################################################
#######################################################
def download(url, data = None):
    while 1:
        if data == None:
            error_msg, url, redirected_url, html = downloader.download(url)
        else:
            error_msg, url, redirected_url, html = downloader.download(url, data)

        if error_msg != None:
            time.sleep(5)
            continue

        time.sleep(5)
        break
    return error_msg, url, redirected_url, html

    ##################################################################3
    ##################################################################
def check_price():
    current_prices = {}
    
    url =  "http://www.kaixin001.com/!stall/!dialog/buygoodsfromsys.php"
    error_msg, url, redirected_url, html = download(url)

    page = WebPage(url, html)

    #print page.doc.items()

    ele = page.doc.findall('.//li')
    for e in ele:
        # goods name
        classes = e.find_class('name')
        name = classes[0].text_content()
        # goods id
        element = e.find(".//input")
        dic= {}
        for k,v in element.items():
            dic[k] = v
        gid = dic['value']
        # good price
        price = e.find_class('price')
        a = price[0].find('.//span')
        price =   a.text_content()
        #
        #print name, gid, price
        current_prices[str(gid).strip()] = int(price)
        #
    return current_prices

def buyprice2db(stallid, prices):
    key = stallid+"B"
    val = kaixindb.select( key )
    #print val
    if val == None:
        item_prices = {}
        for gid,price in prices.items():
            item_prices[gid] = [price]
        kaixindb.insert(key, json.dumps(item_prices))
    else:
        item_prices = json.loads(val)
        for gid,price in prices.items():
            if gid in item_prices:
                if price not in item_prices[gid]:
                    item_prices[gid].append(price)
            else:
                    item_prices[gid] = [price]
        kaixindb.insert(key, json.dumps(item_prices))
    kaixindb.database.sync()####

def best_goods(prices, minp, maxp):
    key = stallid+"B"
    val = kaixindb.select( key )
    item_prices = json.loads(val)
    best = []
    for gid, price in prices.items():
        if gid not in item_prices:
            continue
        mprice = min(item_prices[gid])
        if len(item_prices[gid])> 10 and price <= mprice and price >= minp and price <= maxp:
             best.append(gid)
    return best     
            
def get_stall_id():
    url =  "http://www.kaixin001.com/!stall/!dialog/buygoodsfromsys.php"
    error_msg, url, redirected_url, html = download(url)
    page = WebPage(url, html)

    #@@@@@@@@@@@@@ get stall id
    STALL_ID = None
    elements = page.doc.findall(".//input")
    for e in elements:
        dic = {}
        for k,v in e.items():
            dic[k] = v
        if dic['name'] == "stallid":
            #print dic
            STALL_ID = dic['value']
    return str(STALL_ID).strip()


def buy(goods_id, num):
    url =  "http://www.kaixin001.com/!stall/!dialog/buygoodsfromsys.php"
    error_msg, url, redirected_url, html = download(url)
    page = WebPage(url, html)    
    ######################################
    # select goods
    url, data = page.get_form(0)
    data['goodsid'] = str(goods_id).strip()
    error_msg, url, redirected_url, html = download(url,data)

    ###################################3
    # set num and buy
    page2 = WebPage(url, html)
    url, data = page2.get_form(0)
    dic ={}
    for k,v in data.items():
        dic[k] =v
    dic['num'] = str(num)
    error_msg, url, redirected_url, html = download(url,dic)

    ######################################
    # set price

def set_price(stall_id, goods_id, low_per, high_per):
    url = 'http://www.kaixin001.com/!stall/!dialog/changeprice.php?stallid='+stall_id+'&goodsid='+goods_id
    error_msg, url, redirected_url, html = download(url)

    page = WebPage(url, html)
    es = page.doc.find_class("nomargin")
    e = es[0].find(".//span")
    price = e.text_content()
    if len(price.strip()) == 0:
        return False
    purchase_price =  float(price.strip())
    
    url, data = page.get_form(0)
    dic = {}
    for k,v in data.items():
        dic[k] = v
    dic['dealsetting'] = '1'
    dic['minprice'] = str(int(purchase_price* (1.0 + low_per)))
    dic['idealprice'] = str(int(purchase_price* (1.0 + high_per)))

    #print url, data.items()
    error_msg, url, redirected_url, html = download(url,dic)
     
def get_account():
    url = "http://www.kaixin001.com/!stall/!ajax/account.php"       
    error_msg, url, redirected_url, html = download(url)

    account = json.loads(html)
    stallid = str(account['stallid'])
    cash = int(account['realcash'])
    return stallid, cash


if __name__== "__main__":
    user = sys.argv[1]
    pwd = sys.argv[2]
    ret = login(user, pwd)
    if ret == True:
        print "login into system"

    ############################################33
    selltimer = 1
    sellcnt = 0
    while 1:
        #####SELL#########
        sellcnt += 1
        if sellcnt >= selltimer:
            print "try to sell....", time.ctime()
            gid, price, num = get_buy_info()
            if price > 0 :
                sell(gid, num)
                print 'sell........',gid,num, time.ctime()
            selltimer = random.randint(5,10)
            sellcnt = 0            
            print "Done", time.ctime()

        #####BUY######
        m = time.strftime("%M", time.localtime())
        if m in ["05","35"]:
            print "try to buy...", time.ctime()

            stallid, cash = get_account()
            current_price = check_price()
            buyprice2db(stallid, current_price)
            goods = best_goods(current_price, 300, 1000)
            print goods
            for gid in goods:
                for i in range(3):
                    stallid, cash = get_account()
                    available =  cash/current_price[gid]
                    num = 0 
                    if available > 100:
                        num = 100
                    elif available < 10:
                        continue
                    else:
                        num = int(available)
                    print "buy.......", gid, num, time.ctime()

                    ret = buy(gid, num)

                set_price(stallid, gid, 0.3, 0.3)

            print "done", time.ctime()
        #####SLEEP########
        time.sleep(60)


    """    
    stallid, cash = get_account()
    print stallid, cash
    current_price = check_price()
    print current_price
    buyprice2db(stallid, current_price)
    
    goods = best_goods(current_price, 300, 1000)
    print goods

    """

