import lxml.html    # python-lxml
import urlparse

class WebPage:
    
    ###########################################
    #   WEBPAGE CONSTRUCTOR
    ###########################################
    def __init__(self, url, htmlsrc = None):
        self.url = url
        self.url_redirect = None
        #self.htmlsrc = htmlsrc
        if htmlsrc != None:
            self.html = lxml.html.fromstring(htmlsrc)
        self.hyperlinks = {}
        self.filterlinks = []
        #self.download = None




    #######################################
    # parsing links from html page
    #######################################
    def parse_links(self):
        for elem, attr, link, pos in self.html.iterlinks():
            absolute = urlparse.urljoin(self.url, link.strip())
            #print elem.tag ,attr, absolute, pos
            if elem.tag in self.hyperlinks:
                self.hyperlinks[elem.tag].append(absolute)
            else:
                self.hyperlinks[elem.tag] = [absolute]
        #print lxml.html.tostring(self.html,True)
        return self.hyperlinks

    #######################################
    # filter out unrelated links
    #######################################
    def rm_duplicate(self,seq): 
        # order preserving
        seen = {}
        result = []
        for item in seq:
            if item in seen: continue
            seen[item] = 1
            result.append(item)
        return result

    def filter_links(self,tags=[],patterns=[]):

        self.filterlinks = []
        if len(tags)>0:
            for tag in tags:
                for link in self.hyperlinks[tag]:
                    if len(patterns) == 0:
                        self.filterlinks.append(link)
                    else:
                        for pattern in patterns:
                            if pattern.match(link)!=None:
                                self.filterlinks.append(link)
                                continue
        else:
            for k,v in self.hyperlinks.items():
                for link in v:
                    if len(patterns) == 0:
                        self.filterlinks.append(link)
                    else:
                        for pattern in patterns:
                            if pattern.match(link)!=None:
                                self.filterlinks.append(link)
                                continue

        filterlinks = self.rm_duplicate(self.filterlinks)

        return filterlinks


    def get_htmlcode(self):
        return lxml.html.tostring(self.html)

    #######################################
    # save html code to database
    #######################################
    def html2bdb(self,url, htmldb):
        #value = htmldb.get(self.url)
        if self.url_redirect == None:
            htmldb.put(url,lxml.html.tostring(self.html))
        else:
            pass
            #htmldb.put(url, self.url_redirect)
            #htmldb.put(self.url_redirect, lxml.html.tostring(self.html))

    #######################################
    # save links to database
    #######################################
    
    def pushlinks(links, queuedb, seendb, ):
        for link in links:
            sval = seendb.get(link)
            if sval==None:
                seendb.put(link,"")
                queuedb.append(link)

        if self.url_redirect != None:        
            seendb.put(self.url_redirect,"")
        
    #######################################
    #
    #######################################
    def write2file(self, f):
        pass
        
    #######################################
    #
    #######################################
    def remove_tags(self, on_original_html = True):
        pass

    def search(self, on_original_html = True ):
        pass

    #######################################
    #
    #######################################
    def url_match(self,pattern):
        repattern = re.compile(pattern)
        result = repattern.match(self.suri)
        if result == None:
            return False
        else:
            return True 

    def getform(self):
        return self.html.forms[0]


    def fillform(form, keyval):
        for k,v in keyval.items():
            form.fields[k] = v
        return form

    def submitform(self, form ):
        form.action = urlparse.urljoin(self.url, form.action)
        response = lxml.html.submit_form( form )
        #the_page = response.read()
        #return the_page
        url = response.geturl()
        return url

if __name__ == "__main__":
    from download_manager import DownloadManager
    url = "http://kaixin001.com/"
    page = WebPage(url)
    page.download()
    print page.doc.forms[0].action

    for k,v in page.doc.forms[0].fields.items():
        print k,v
        #print lxml.html.tostring( self.doc )

    #print page.doc.forms
    #for k,v in page.doc.forms.items():
    #    print k,v
