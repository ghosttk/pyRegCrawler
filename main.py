# -*- coding: utf-8 -*-
import urllib.request
from urllib import error, parse
import string, re,  os, sys
import sqlite3

class RegParser():
    def __init__(self, Url, count):
        self.baseUrl, pUrl = self.getBaseUrl(Url)
        if pUrl:
            print(pUrl)
        self.count =count
        self.strToWrite = []
        self.conn = sqlite3.connect('conf.db')
        self.cur = self.conn.cursor()
        self.cur.execute('select * from param where base=?', (self.baseUrl,))
        record = self.cur.fetchone()
        self.url = record[2]
        self.BodyPattern = record[3]
        self.UrlPattern = record[4]
        self.trunkPattern = record[5]
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        filename = re.search('\/(\d+)\.htm', self.url).group(1)
        self.fo = open(filename+'.txt', 'a+')
    def getBaseUrl(self, url):
        basePattern = '(https?://.*?/)(.*)'
        res = re.search(basePattern, url)
        return res.group(1), res.group(2)
    def __del__(self):
        self.fo.writelines(self.strToWrite)
        self.fo.close()
        
        #self.cur.execute('INSERT INTO PARAM VALUES (?,?,?,?,?,?)', (1,self.baseUrl,self.url,self.BodyPattern,self.UrlPattern,self.trunkPattern))
        print('update ...'+self.url)
        self.cur.execute('update param set url=? where base=?',(self.url, self.baseUrl))
        self.conn.commit()
        self.conn.close()
    def parseBaseUrl(self, url):
        baseUrl = re.match('https?://.*?/', url).group()
        return baseUrl
    def fmtBodyString(self, strBody):
        result = re.sub(self.trunkPattern, '', strBody)
        return result
    def parseHtml(self):
        self.url = urllib.parse.quote(self.url, safe=string.printable)
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
        self.url = nextLink
        return body, nextLink
if __name__ == "__main__":
     #baseUrl = 'http://www.jokeji.cn/'
     baseUrl = sys.argv[1]
     count = int(sys.argv[2])
     myRegParser = RegParser(baseUrl, count)
     while(myRegParser.url !='' and count>0):
         print('connecting...'+myRegParser.url)
         bodyString, nextLink = myRegParser.parseHtml()
         myRegParser.strToWrite.append(bodyString)
         count-=1

