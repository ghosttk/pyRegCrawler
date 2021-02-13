# -*- coding: utf-8 -*-
import urllib.request
from urllib import error, parse
import string
import re

def parseHtml(url, BodyPattern, UrlPattern):
     url = urllib.parse.quote(url, safe=string.printable)
     try:
         res = urllib.request.urlopen(url)
     except urllib.error.URLError as e:
         print(e)
     Content = res.read().decode('gb2312', 'ignore')
     #print(Content)
     body = re.findall(BodyPattern, Content, re.S)
     body = re.findall('[\u4e00-\u9fa5]+', body[0])
     nextLink = re.search(UrlPattern, Content, re.S).group(1)
     if nextLink != '':
         BaseUrl = re.match('https*://.*?/', url).group()
         nextLink = re.sub('\.\./\.\./', '',  nextLink)
         nextLink = BaseUrl + nextLink
     return body, nextLink
if __name__ == "__main__":
     url = 'http://www.jokeji.cn/jokehtml/mj/202101241746485.htm'
     BodyPattern = '<span id=\"text110\">(.*)?<\/span>'
     UrlPattern = '<div class=zw_page1>.*?<a href=\"(.*?)\">'
     body, nextLink = parseHtml(url, BodyPattern, UrlPattern)
     while nextLink !='':
         body, nextLink = parseHtml(nextLink, BodyPattern, UrlPattern)
         print(body)
