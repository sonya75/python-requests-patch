from requests.adapters import HTTPAdapter
import user_agents
import urlparse
from collections import OrderedDict
def addrequiredheaders(req):
    d=req.headers
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    if "User-Agent" not in d:
        d["User-Agent"]=useragent
    e=user_agents.parse(d["User-Agent"])
    if e.browser.family=="Python Requests":
        d["User-Agent"]=useragent
    if "Host" not in d:
        d["Host"]=urlparse.urlparse(req.url).netloc
def modifyheaders(headers):
    browser=user_agents.parse(headers["User-Agent"]).browser
    if browser.family not in ["Chrome","Firefox","Opera"]:
        print "Currently only works with Firefox and Opera"
        raise Exception("Browser not recognized")
    if browser.family=="Chrome" or browser.family=="Other":
        defaultheaders=["Host","Connection","Upgrade-Insecure-Requests","User-Agent","Accept","Accept-Encoding","Accept-Language"]
        defaultheadervalues={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Language":"en-US,en;q=0.8","Accept-Encoding":"gzip, deflate, sdch","Connection":"keep-alive","Upgrade-Insecure-Requests":"1"}
        for p in defaultheaders:
            # Default headers:
            # {'Connection': 'keep-alive', 'Host': 'httpbin.org', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
            # "if p not in headers" would prevent "Accept" and "Accept-Encoding" from being set
            if p not in ["Host"]:
                headers[p]=defaultheadervalues[p]
        headerorder=["Host","Connection","Upgrade-Insecure-Requests","User-Agent","Accept","Referer","Accept-Encoding","Accept-Language","Cookie"]
        finalheader=OrderedDict()
        for q in headerorder:
            if q in headers:
                finalheader[q]=headers[q]
        for q in headers:
            finalheader[q]=headers[q]
        return finalheader
    if browser.family=="Firefox":
        defaultheaders=["Host","User-Agent","Accept","Accept-Language","Accept-Encoding","Connection","Upgrade-Insecure-Requests"]
        defaultheadervalues={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate","Connection":"keep-alive","Upgrade-Insecure-Requests":"1"}
        #Python-Requests uses */* as the default Accept header, so changing it to the default values of different browsers
        if headers["Accept"]=="*/*":
            headers["Accept"]=defaultheadervalues["Accept"]
        for p in defaultheaders:
            if p not in headers:
                headers[p]=defaultheadervalues[p]
        headerorder=["Host","User-Agent","Accept","Accept-Language","Accept-Encoding","Referer","Cookie","Connection","Upgrade-Insecure-Requests"]
        finalheader=OrderedDict()
        for q in headerorder:
            if q in headers:
                finalheader[q]=headers[q]
        for q in headers:
            finalheader[q]=headers[q]
        return finalheader
    if browser.family=="Opera":
        defaultheaders=["Host","User-Agent","Accept","Accept-Language","Accept-Encoding","Connection","Upgrade-Insecure-Requests","Cache-Control"]
        defaultheadervalues={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991","Accept":"application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5","Accept-Language":"en-US,en;q=0.8","Accept-Encoding":"gzip, deflate, sdch","Connection":"keep-alive","Upgrade-Insecure-Requests":"1"}
        #Python-Requests uses */* as the default Accept header, so changing it to the default values of different browsers
        if headers["Accept"]=="*/*":
            headers["Accept"]=defaultheadervalues["Accept"]
        for p in defaultheaders:
            if p not in headers:
                headers[p]=defaultheadervalues[p]
        headerorder=["Host","Connection","Upgrade-Insecure-Requests","User-Agent","Accept","Accept-Encoding","Accept-Language","Cookie"]
        finalheader=OrderedDict()
        for q in headerorder:
            if q in headers:
                finalheader[q]=headers[q]
        for q in headers:
            finalheader[q]=headers[q]
        return finalheader
def modded_add_headers(adapter,req,**kwargs):
    addrequiredheaders(req)
    req.headers=modifyheaders(req.headers)


HTTPAdapter.add_headers=modded_add_headers
