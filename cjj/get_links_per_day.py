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

def get_next_page(url):
    """获取下一个分页的URL"""
    html = urlopen(url)
    bsObj=BeautifulSoup(html)
    print(bsObj)
    try:
        for link in bsObj.findAll("span",{"class":"next unavailable"}):
            if link is not None:
                return None
    finally:
        for link in bsObj.findAll("a",{"class":"next"}):
            next_page = link.attrs['href']
    return next_page.strip()[2:]

def get_links_per_day(url):
    """获取某一天的全部拍卖商品详细页面的链接"""
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll("script", {"id":"sf-item-list-data"}):
        dict_links = link.get_text()
        res_json = json.loads(dict_links)
        print(res_json)
        for link in res_json["data"]:
            print(link["itemUrl"])
    print(get_next_page(url))
    while(get_next_page(url)):
        url = "https://"+get_next_page(url)
        print(url)
        html = urlopen(url)
        bsObj = BeautifulSoup(html)
        for link in bsObj.findAll("script", {"id": "sf-item-list-data"}):
            dict_links = link.get_text()
            res_json = json.loads(dict_links)
            print(res_json)
            for link in res_json["data"]:
                print(link["itemUrl"])

url= "https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"
# print(get_next_page("https://sf.taobao.com/calendar/0_1451577600000_-1.htm?page=11"))
print (get_next_page(url))
# print (get_links_per_day(url))
