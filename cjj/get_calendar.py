# coding:utf-8
"""
create on Jan 5,2017 by Wenyan Yu

获取日历中每天的拍卖商品列表首页面

从2016年1月1日开始到2016年12月31日截止，一共一年的时间：
https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000 2016.01.01
https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451664000000 2016.01.02
https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451750400000 2016.01.03
https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451836800000 2016.01.04
https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451923200000 2016.01.05
.
.
.
https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1483113600000 2016.12.31


"""
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import csv


def get_calendar(url):
    """获取日历中的拍卖商品列表首页面URL"""
    links_list = []
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        print(bsObj)

    except AttributeError as e:
        return None
    return links_list

url = "https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"
print(get_calendar(url))