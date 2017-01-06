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

1451577600 表示2016年１月1日与Epoch时间也就是Unix 时间戳之间所差的秒数
Epoch 1970-01-01 00:00:00 UTC


"""
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import csv
import time

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


def get_calendar_links(start_time_epoch, end_time_epoch):
    """获取指定时间段的拍卖商品列表的日历链接"""
    calendar_links_list =[]
    print("开始时间戳：", start_time_epoch)
    print("结束时间戳：", end_time_epoch)

    if start_time_epoch > end_time_epoch:
        print("您输入的时间区间有有误，请重新输入！")
        return None

    while(start_time_epoch<=end_time_epoch):
        current_time = start_time_epoch
        link = "https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate="+str(current_time)+"000"
        print(link)
        calendar_links_list.append(link)
        start_time_epoch += 86400
    return calendar_links_list

url = "https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"
# print(get_calendar(url))
# second = 1451577600
# second =1451664000
# t= 1451577600
# print(time.localtime(t))
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t)))
# print(time.time())
# help(time)
# print(1451577600 - 1451664000) # output:86400

import datetime

start_time = datetime.datetime(2016,1, 1, 0, 0, 0)
# print("开始时间：", start_time, round(time.mktime(start_time.timetuple())))
start_time_epoch = round(time.mktime(start_time.timetuple()))
end_time = datetime.datetime(2016,2, 1, 0, 0, 0)
# print("结束时间：", end_time, round(time.mktime(end_time.timetuple())))
end_time_epoch= round(time.mktime(end_time.timetuple()))

print(get_calendar_links(start_time_epoch, end_time_epoch))
# help(time.mktime)
"""
mktime(...)
    mktime(tuple) -> floating point number

    Convert a time tuple in local time to seconds since the Epoch.
    Note that mktime(gmtime(0)) will not generally return zero for most
    time zones; instead the returned value will either be equal to that
    of the timezone or altzone attributes on the time module.
"""
# help(start_time.timetuple)
"""
timetuple(...) method of datetime.datetime instance
    Return time tuple, compatible with time.localtime().

"""



