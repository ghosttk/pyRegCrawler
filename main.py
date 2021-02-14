# -*- coding: utf-8 -*-
import urllib.request
from urllib import error, parse
import string, re, configparser, os


class RegParser():
    def __init__(self, baseUrl, count):
        self.baseUrl = baseUrl
        self.count =count
        self.cp = configparser.ConfigParser()
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        config_file = curr_dir + os.sep + "params.conf"
        cp = configparser.ConfigParser()
        self.cp.read(config_file)
        urlToQoute = self.cp.get(self.baseUrl, 'url')
        self.url = urllib.parse.quote(urlToQoute, safe=string.printable)
        self.BodyPattern = self.cp.get(self.baseUrl, 'BodyPattern')
        self.UrlPattern = self.cp.get(self.baseUrl, 'UrlPattern')
    def parseBaseUrl(self, url):
        baseUrl = re.match('https?://.*?/', url).group()
        return baseUrl
    def parseHtml(self):
        try:
            res = urllib.request.urlopen(self.url)
        except urllib.error.URLError as e:
            print(e)
        Content = res.read().decode('gb2312', 'ignore')
        #print(Content)
        body = re.findall(self.BodyPattern, Content, re.S)
        body = re.findall('[\u4e00-\u9fa5]+', body[0])
        nextLink = re.search(self.UrlPattern, Content, re.S).group(1)
        if nextLink != '':
            nextLink = re.sub('\.\./\.\./', '',  nextLink)
            nextLink = self.baseUrl + nextLink
        return body, nextLink
if __name__ == "__main__":
     baseUrl = 'http://www.jokeji.cn/'
     myRegParser = RegParser(baseUrl, 3)
     print(myRegParser.parseHtml())
     '''
     BodyPattern = '<span id=\"text110\">(.*)?<\/span>'
     Pattern = '<div class=zw_page1>.*?<a href=\"(.*?)\">'
     body, nextLink = parseHtml(url, BodyPattern, UrlPattern)
     while nextLink !='':
         body, nextLink = parseHtml(nextLink, BodyPattern, UrlPattern)
         print(body)
     '''
