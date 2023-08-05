__author__ = 'Trung'

import requests
import requests.utils, pickle
import os,sys
if sys.version_info <= (3,0,0):
    from urlparse import urlsplit as urlsplit
else:
    from urllib.parse import urlsplit

from requests.cookies import merge_cookies
import random

available_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
                    ]

class HttpRequestHelper:

    def __init__(self):
        self.header = {}
        self.cookies = {}
        self.content = {}
        self.payload = {}
        self.url = ''
        r = random.randint(0, len(available_agents)-1)
        self.userAgent = available_agents[r]
        self.referer=None
        self.__useCookieFile = None
        self.cookiePath = None
        self.__session = requests.Session()
        self.timeout = 30

    def setHeader(self, header):
        self.header = header

    def setCookies(self, cookie):
        self.cookies = cookie
        self.__useCookieFile = False

    def useCookieFile(self, use=True, cookieName='cookie'):
        self.__useCookieFile = use
        self.cookiePath = 'cookie_' + cookieName

    def setReferer(self, referer):
        self.referer = referer
        self.header['Referer'] = referer

    def setPostField(self, data):
        self.content = data

    def addHeader(self, hString):
        entries = hString.split("\n")
        for entry in entries:
            temp = entry.split(":", 1)
            if (len(temp) > 1):
                key = temp[0].strip()
                value = temp[1].strip()
                self.header[key] = value

    def setUserAgent(self, agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"):
        self.userAgent = agent

    def __saveCookie(self, cookieObj, path):
        with open(path, 'wb') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(cookieObj), f)

    def __loadCookie(self, path):
        try:
            with open(path, "rb") as f:
                content = pickle.load(f)
                if content:
                    return requests.utils.cookiejar_from_dict(content)
        except IOError:
            pass
        return None

    def __getCookieStringFromFile(self, path):
        str = open(path, 'rb')
        lines = str.split("\n")
        result = ''
        for line in lines:
            w = line.split("\t")
            if (len(w) > 5):
                result = result + w[5].strip() + '=' + w[6].strip() + '; '
        return result

    def get(self, url, allowRedirect = True, stream=False):
        self.setPostField(None)
        return self.send(url, allowRedirect, stream=stream)

    def post(self, url, allowRedirect = True, format=None):
        return self.send(url, allowRedirect, format=None)

    def postWithFiles(self, url, allowRedirect = True, files = None):
        return self.send(url, allowRedirect, files)

    def send(self, url, allowRedirect = True, files=None, stream=False, format=None):
        if not self.referer:
            self.referer = urlsplit( url ).netloc

        if not 'Referer' in self.header:
            self.header['Referer'] = self.referer

        if not 'Host' in self.header:
            self.header['Host'] = self.referer

        if self.__useCookieFile and not self.__session.cookies:
            self.cookies = self.__loadCookie(self.cookiePath)
        requestType = "GET"
        if self.content:
            requestType = "POST"
        if self.userAgent:
            self.header['User-Agent'] = self.userAgent

        result = "EMPTY"
        meta_param = {
            "url": url, "params": self.payload,
            "cookies": self.cookies, "headers": self.header,
            "allow_redirects": allowRedirect, "timeout": self.timeout,
            "stream": stream
        }

        if requestType == "GET":
            result = self.__session.get(**meta_param)

        elif requestType == "POST":
            if files:
                meta_param['files'] = files
            if format and format.lower() == 'json':
                meta_param['json'] = self.content
            else:
                meta_param['data'] = self.content
            result = self.__session.post(**meta_param)

        if not self.cookies:
            self.cookies = self.__session.cookies
        else:
            self.cookies = merge_cookies(self.cookies, self.__session.cookies)

        if (self.__useCookieFile):
            self.__saveCookie(self.cookies, self.cookiePath)

        return result

# unit test
if __name__ == '__main__':
    request = HttpRequestHelper()
    request.addHeader("Accept: text/html, application/xhtml+xml, image/jxr, */*")
    request.addHeader("Accept-Language: en-US,en;q=0.7,vi;q=0.3")
    request.useCookieFile(True)
    response = request.get('http://stackoverflow.com/', True)
    #cookie = requests.utils.dict_from_cookiejar(response.cookies)
    print(response.content)



