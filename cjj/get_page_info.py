# coding:utf-8
"""
create on Jan 04,2017 by Wenyan Yu
function: a web crawler for PaiMai info

只考虑历史拍卖记录，已成功拍卖的以及流拍的商品，不考虑正在拍卖的商品。

需要抓取商品信息如下：
标题，结束时间，拍卖状态，成交价格，报名人数，提醒人数，围观次数，起拍价，加价幅度，保证金，佣金，延时周期，保留价，送拍机构，特色服务
"""
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import csv
# Retrieve HTML string from the URL


def get_title(url):
    """获取拍卖的标题"""
    try:
        html=urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj= BeautifulSoup(html.read())
        title=bsObj.body.h1.get_text()
    except AttributeError as e:
        return None
    return title

def get_time(url):
    """获取拍卖结束的时间，如果拍卖成功则为成交时间，如果流拍则为结束时间"""
    try:
        html=urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    time = None
    try:
        bsObj = BeautifulSoup(html.read())
        timelist = bsObj.findAll("span", {"class": "countdown J_TimeLeft"})
        for i in timelist:
            time = i.get_text()
    except AttributeError as e:
        return None
    return time

def get_state(url):
    """获取商品拍卖的状态"""
    try:
        html=urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj= BeautifulSoup(html.read())
        statelist=bsObj.findAll("span", {"class": "title"})
        # print (statelist) 此处会获取到两个匹配项　[<span class="title">成交价</span>, <span class="title over-title">成交时间</span>]
        for i in statelist[0:1]: # 使用列表的切片技术获取到第一个列表项
            state = i.get_text()
    except AttributeError as e:
        return None
    if state=="成交价":
        return "已成交"
    else:
        return "流拍"

def get_price(url):
    """获取商品拍卖价格,不考虑正在拍卖的商品"""
    try:
        html=urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj= BeautifulSoup(html.read())
        pricelist=bsObj.findAll("span", {"class": "pm-current-price J_Price"})
        # print (pricelist)
        for i in pricelist:
            price = i.get_text()
    except AttributeError as e:
        return None
    return price

def get_apply(url):
    """获取拍卖商品的报名人数"""
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        applylist = bsObj.findAll("em", {"class": "J_Applyer"})
        # print (apply)
        for i in applylist:
            apply=i.get_text()

    except AttributeError as e:
        return None
    return apply

def get_remind(url):
    """获取拍卖商品的设置提醒人数"""
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        remindlist = bsObj.findAll("span", {"class": "pm-reminder i-b"})
        # print (remindlist)
        remind = remindlist[0].get_text()
        remind = "".join(re.findall("[0-9]+", remind)) # 此处用正则表达式获取信息中的数字
    except AttributeError as e:
        return None
    return remind

def get_surround(url):
    """获取拍卖商品的围观人数"""
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        surroundlist = bsObj.findAll("em", {"id": "J_Looker"})
        # print (surroundlist)
        surround = surroundlist[0].get_text()
    except AttributeError as e:
        return None
    return surround

# title = get_title("http://www.pythonscraping.com/exercises/exercise1.html")
# url = "https://sf.taobao.com/sf_item/537674355828.htm?spm=a213w.7398552.paiList.3.e6cNNe"
# url = "https://sf.taobao.com/sf_item/537976732316.htm?spm=a213w.7398552.paiList.1.e6cNNe"
# url = "https://sf.taobao.com/sf_item/525351764416.htm?spm=a213w.7398552.paiList.1.3gRZ06"
url = "https://sf.taobao.com/sf_item/525612660941.htm?spm=a213w.7398552.paiList.1.WjcE6s"
title = get_title(url)

if title == None:
    print("Title could not be found")
elif get_time(url) == None:
    print("该拍卖商品已撤回")
else:
    print("标题:", title)
    print("结束时间:", get_time(url))
    print("状态:", get_state(url))
    print("价格:", get_price(url).strip())
    print("报名人数:", get_apply(url))
    print("提醒人数:", get_remind(url))
    print("围观人数:", get_surround(url))
    page_info = open("page_info.csv", "w+")
    try:
        writer = csv.writer(page_info)
        writer.writerow((title.strip(), get_time(url), get_state(url), get_price(url).strip(url), get_apply(url), get_remind(url), get_surround(url)))
    finally:
        page_info.close()



