# -*- coding: utf-8 -*-
import urllib.request
from urllib import error, parse
import string, re, configparser, os, sys


class RegParser():
    def __init__(self, baseUrl, count):
        self.baseUrl = baseUrl
        self.count =count
        self.strToWrite = []
        self.cp = configparser.ConfigParser()
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        config_file = curr_dir + os.sep + "params.conf"
        self.cp.read(config_file)
        urlToQoute = self.cp.get(self.baseUrl, 'url')
        filename = re.search('\/(\d+)\.htm', urlToQoute).group(1)
        self.fo = open(filename+'.txt', 'a+')
        self.url = urllib.parse.quote(urlToQoute, safe=string.printable)
        self.BodyPattern = self.cp.get(self.baseUrl, 'BodyPattern')
        self.UrlPattern = self.cp.get(self.baseUrl, 'UrlPattern')
        self.trunkPattern = self.cp.get(self.baseUrl, 'trunkPattern')
        self.nextLink = self.cp.get(self.baseUrl, 'url')
    def __del__(self):
        self.fo.writelines(self.strToWrite)
        self.fo.close()
        self.cp.set(self.baseUrl, 'url', self.nextLink)
    def parseBaseUrl(self, url):
        baseUrl = re.match('https?://.*?/', url).group()
        return baseUrl
    def fmtBodyString(self, strBody):
        result = re.sub(self.trunkPattern, '', strBody)
        return result
    def parseHtml(self):
        try:
            res = urllib.request.urlopen(self.url)
        except urllib.error.URLError as e:
            print(e)
        Content = res.read().decode('gb2312', 'ignore')
        body = re.findall(self.BodyPattern, Content, re.S)[0]
        body = self.fmtBodyString(body)
        #body = re.findall('[\u4e00-\u9fa5]+', body[0])
        nextLink = re.search(self.UrlPattern, Content, re.S).group(1)
        if nextLink != '':
            nextLink = re.sub('\.\./\.\./', '',  nextLink)
            nextLink = self.baseUrl + nextLink
        self.nextLink = nextLink
        print(nextLink)
        return body, nextLink
if __name__ == "__main__":
     #baseUrl = 'http://www.jokeji.cn/'
     baseUrl = sys.argv[1]
     count = int(sys.argv[2])
     myRegParser = RegParser(baseUrl, count)
     bodyString, nextLink = myRegParser.parseHtml()
     myRegParser.strToWrite.append(bodyString)
     while(nextLink!='' and count>0):
         count-=1
         myRegParser.url = urllib.parse.quote(nextLink, safe=string.printable)
         bodyString, nextLink = myRegParser.parseHtml()
         myRegParser.strToWrite.append(bodyString)

