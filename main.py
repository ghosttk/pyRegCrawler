import urllib.request
import re

if __name__ == "__main__":
     url = 'http://www.jokeji.cn/jokehtml/mj/202101241746485.htm'
     res = urllib.request.urlopen(url)
     print(res.read().decode('gb2312'))
