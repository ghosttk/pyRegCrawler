import urllib.request
import re

def parseHtml(url,BodyPattern):
     res = urllib.request.urlopen(url)
     Content = res.read().decode('gb2312', errors='ignore')
     #print(Content)
     body = re.findall(BodyPattern, Content, re.S)
     nextLink = '66'
     return body, nextLink
if __name__ == "__main__":
     url = 'http://www.jokeji.cn/jokehtml/mj/202101241746485.htm'
     BodyPattern = '<span id=\"text110\">(.*)?<\/span>'
     body, nextLink = parseHtml(url,BodyPattern)
     print(body)
