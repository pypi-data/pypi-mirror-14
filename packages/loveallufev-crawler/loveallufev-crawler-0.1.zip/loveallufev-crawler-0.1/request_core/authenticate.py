__author__ = 'Trung'


import requests
import sys

if sys.version_info <= (3,0,0):
    import request
    from urlparse import urlsplit as urlsplit
else:
    from urllib.parse import urlsplit
    from . import request

import datetime
import pickle



#from lxml.html import soupparser

# Must install Beautiful Soup
# pip install beautifulsoup4
# install lxml: https://pypi.python.org/pypi/lxml/3.3.5#downloads
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

class Authentication:
    def __init__(self, username='', password=''):
        self.username = username
        self.password = password
        self.httpRequest = request.HttpRequestHelper()
        self.httpRequest.useCookieFile(True, 'authen')
        self.expireTime = 30 # minutes
        self.__metadata = {}
        self.__init = False

    def __initMetadata(self):
        try:
            if not self.__init:
                with open('__metadata', "rb") as f:
                    self.__metadata = pickle.load(f)
        except IOError:
            pass

    def login(self, url, type="POST"):
        if not self.__init:
            self.__initMetadata()

        result = self.httpRequest.post(url, True)

        if result.status_code == requests.codes.ok or \
            result.status_code == requests.codes.found or \
            result.status_code == requests.codes.moved_permanently:
            #print(result.content)
            parsed_uri = urlsplit( url )
            hostname = parsed_uri.netloc
            self.__metadata[hostname]={}
            self.__metadata[hostname]['last_login'] = datetime.datetime.utcnow()
            self.__metadata[hostname]['expire_time'] = self.expireTime
            #with open('__metadata', 'wb', encoding='utf-8') as f:
            with open('__metadata', 'wb') as f:
                pickle.dump(self.__metadata, f)

    def checkAndLogin(self, url):
        if not self.checkCookieValid(urlsplit( url ).netloc):
            self.login(url)

    def checkCookieValid(self, hostname):
        if not self.__init:
            self.__initMetadata()
        try:
            now = datetime.datetime.utcnow()
            diff = now - self.__metadata[hostname]['last_login']
            import os
            if not os._exists(self.httpRequest.cookiePath):
                print("there is no cookie for authentication at ", self.httpRequest.cookiePath)
                return False
            return not diff.total_seconds() // 60 > self.__metadata[hostname]['expire_time']
        except Exception:
            return False

if __name__ == "__main__":
    import xml.etree.ElementTree as ET
    from bs4 import BeautifulSoup
    # lxml try to import BeautifulSoup 3 -> cheat him here
    import sys, bs4
    sys.modules['BeautifulSoup'] = bs4
    auth = Authentication()
    auth.username = ''
    auth.password = ''
    # data = {
    #         "username" : "h01309001dungntt", \
    #         "passwd" : "triemtriem", \
    #         "option" : "login", \
    #         "op2" : "login", \
    #         "return" : "index.php", \
    #         "message" : "0", \
    #         "Submit" : "??ng nh?p"
    # }
    page = auth.httpRequest.send('http://nauthenao.com/dang-nhap/')
    # page = auth.httpRequest.send('http://tuoitre.vn')
    #import xml.etree.ElementTree as ET

    soup = BeautifulSoup(page.content, "html.parser")

    # soup.prettify().encode("utf-8")

    parentTree = soupparser.fromstring(soup.body)
    # parentTree = soupparser.fromstring(soup.body.encode("utf-8"))
    nonce = parentTree.xpath("//input[@id='login_form_nonce']/@value")

    data = {
        "log" : "admin",
        "pwd": "trungyeumi1989",
        "rememberme" : "on",
        "login_form_nonce": nonce,
        "_wp_http_referer":"%2Fdang-nhap%2F",
        "redirect_to" :"%2Fdang-nhap%2F",
        "login":"%C4%90%C4%83ng+nh%E1%BA%ADp"
    }

    auth.httpRequest.content = data

    auth.checkAndLogin('http://nauthenao.com/dang-nhap/')
