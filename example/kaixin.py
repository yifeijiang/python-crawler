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
    if 'price' not in sales['goods']:
        return 0,0,0
    else:
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

######################################
##
######################################
def buyprice2db(kaixindb, stallid, prices):
    #key = stallid+"B"
    #val = kaixindb.select( key )
    for gid,price in prices.items():
        key = str("B"+gid.strip())
        val = kaixindb.select( key )
        #
        if val == None:
            price_list = [price]
            kaixindb.insert(key, json.dumps(price_list))
        else:
            price_list = json.loads(val)
            if price not in price_list:
                price_list.append(price)
                price_list = sorted(price_list)
                kaixindb.insert(key, json.dumps(price_list))

    kaixindb.database.sync()####

def best_goods(kaixindb, stallid, prices, minp, maxp):
    #key = stallid+"B"
    #val = kaixindb.select( key )
    #item_prices = json.loads(val)
    best = []
    for gid, price in prices.items():
        key = str("B"+gid.strip())
        val = kaixindb.select( key )
        if val ==None:
            continue
        price_list = json.loads(val)
        if len(price_list)> 10 and price > minp and price < maxp:
            if price in price_list:
                i = price_list.index(price)
                if float(i)/float(len(price_list)) <= 0.1:
                    best.append(gid)
                    #print price_list
                    #print price
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
    try:
        url, data = page.get_form(0)
        data['goodsid'] = str(goods_id).strip()
        error_msg, url, redirected_url, html = download(url,data)
    except:
        return False
    ###################################3
    # set num and buy
    try:
        page2 = WebPage(url, html)    
        url, data = page2.get_form(0)
    except:
        return False # excessed the maxmum purchase per hour
    dic ={}
    for k,v in data.items():
        dic[k] =v
    dic['num'] = str(num)
    error_msg, url, redirected_url, html = download(url,dic)

    ######################################
    # set price
def buy_goods(goods,current_price):
    #print goods
    for gid in goods:
        for i in range(5):
            stallid, cash = get_account()
            available =  cash/current_price[gid]
            num = 0 
            if available > 100:
                num = 100
            elif available < 10:
                continue
            else:
                num = int(available)
            print "BUY", gid, num, time.ctime()

            ret = buy(gid, num)
            if ret == False:
                break

        set_price(stallid, gid, 0.2, 0.3)

def price_ajust(p):
    sp =  str(p)
    l = len(sp)
    if l >2:
        p= int(p/(10**(l-2)))
        p = p * (10**(l-2))
    return p


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
    lprice = int(purchase_price* (1.0 + low_per))
    lprice = price_ajust(lprice)
    dic['minprice'] = str(lprice)
    hprice = int(purchase_price* (1.0 + high_per))
    hprice = price_ajust(hprice)    
    dic['idealprice'] = str(hprice)
    dic['higglenum'] = "5"


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
    buy_low  = int(sys.argv[3])
    buy_high =  int(sys.argv[4])

    ret = login(user, pwd)
    if ret == True:
        print "login into system"

    kaixindb =  WebpageDB('stall.db')
    ############################################33
    selltimer = 1
    sellcnt = 0
    init = True
    while 1:
        #####SELL#########
        sellcnt += 1
        if sellcnt >= selltimer:
            print "================================"
            print "try to sell....", time.ctime()
            gid, price, num = get_buy_info()
            if price > 0 :
                sell(gid, num)
                print 'SELL',gid,num, time.ctime()
            selltimer = random.randint(5,10)
            sellcnt = 0            
            print "Done", time.ctime()

        #####BUY######
        m = time.strftime("%M", time.localtime())
        if m in ["09","38"] or init == True:
            init = False
            print "================================"
            print "try to buy...", time.ctime()

            stallid, cash = get_account()
            current_price = check_price()
            buyprice2db(kaixindb, stallid, current_price)
            goods = best_goods(kaixindb, stallid,current_price, buy_low, buy_high)
            print goods
            buy_goods(goods, current_price)

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

