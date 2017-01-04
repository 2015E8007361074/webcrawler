# coding:utf-8
"""
create on Jan 4,2017 by Wenyan Yu
获取每天的司法拍卖页面中的拍卖商品详细页面的链接，以2016年1月1日为例
url:https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000

获取该页面中的所有拍卖商品的详细页面链接，包括所有的分页

"""

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import json

html = urlopen("https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000")
bsObj = BeautifulSoup(html)
# print(bsObj)
"""
for link in bsObj.findAll("a", href=re.compile("^\/\/sf\."),limit=1):
    if 'href' in link.attrs:
        print(link.attrs['href'])
"""
for link in bsObj.findAll("script",{"id":"sf-item-list-data"} ):
    dict_links = link.get_text()
    res_json = json.loads(dict_links)
    # print(json.dumps(res_json, indent=4))
    print (res_json)



