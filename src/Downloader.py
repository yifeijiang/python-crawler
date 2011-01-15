import urllib2
import urllib
import cookielib
import socket

SOCKET_DEFAULT_TIMEOUT = 30

class Downloader:
    def __init__(cookie = None, timeout = None):
        # cookie
        if cookie == None:
            self.cookie = cookielib.LWPCookieJar() 
        else:
            self.cookie = cookie
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler, urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        # socket timeout
        if timeout == None:
            timeout = SOCKET_DEFAULT_TIMEOUT
            socket.setdefaulttimeout(timeout)
        

    ############################################
    #     download the html page from server. 
    ############################################
    def download(self, data=None):
        # 1. URL Request Head
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        if data != None:
            req = urllib2.Request(self.url, urllib.urlencode(data), headers)
        else:
            req = urllib2.Request(self.url, data, headers)
        # 2. URL Request
        try:
            response = urllib2.urlopen(req)
            self.download = 'url-opened'
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                #raise HtmlPageError('[fetch] failed to reach a server.' + \
                #            ' Reason: '+ str(e.reason) )
                self.download = 'network-error'
            elif hasattr(e, 'code'):
                #raise HtmlPageError('[fetch] server couldn\'t fulfill the request.'+\
                #            ' Error code: '+ str(e.code) )
                self.download = 'server-error'
            else:
                #raise HtmlPageError('[fetch] URLError, unknown reason.')
                self.download = 'other-error'
        except KeyboardInterrupt:
            raise
        except:
            #raise HtmlPageError('[fetch] Unexpected urlopen() error: ' + 
            #            str(sys.exc_info()[0]) )
            self.download = 'urlopen-error'
        
        # 3. Read Html 
        try:
            the_page = response.read()
            self.download = True
        except KeyboardInterrupt:
            raise
        except:
            #raise HtmlPageError('[fetch] Unexpected response.read() error: ' + \
            #            str(sys.exc_info()[0]) )
            self.download = 'reading-error'

        # 4. check if there is a redirect
        if self.download !=True:
            f = open("undownload.dat", 'a')
            f.write(time.strftime("%Y/%m/%d %H:%M:%S") + "\t" + self.download + "\t" + self.url + "\n")
            f.close()
            return self.download

        nurl = response.geturl()
        if self.url != nurl:
            self.url_redirect = nurl
        else:
            self.url_redirect = None            
        
        # 5. generate lxml.html object for future processing
        self.html = lxml.html.fromstring(the_page)
        return True
