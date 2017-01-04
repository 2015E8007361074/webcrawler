# coding:utf-8
"""
create on Jan 04,2017 by Wenyan Yu
function: a web crawler for PaiMai info

只考虑历史拍卖记录，已成功拍卖的以及流拍的商品，不考虑正在拍卖的商品。

需要抓取商品信息如下：
标题，结束时间，是否成交，成交价格，报名人数，提醒人数，围观次数，起拍价，评估价，保证金，加价幅度，竞价周期，延时周期，保留价
"""
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
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
        print (surroundlist)
        surround = surroundlist[0].get_text()
    except AttributeError as e:
        return None
    return surround

# title = get_title("http://www.pythonscraping.com/exercises/exercise1.html")
url = "https://sf.taobao.com/sf_item/537674355828.htm?spm=a213w.7398552.paiList.3.e6cNNe"
# url = "https://sf.taobao.com/sf_item/537976732316.htm?spm=a213w.7398552.paiList.1.e6cNNe"
title = get_title(url)
time = get_time(url)
state = get_state(url)
price = get_price(url)
apply = get_apply(url)
remind = get_remind(url)
surround = get_surround(url)

if title == None:
    print("Title could not be found")
else:
    print("标题:", title)
    print("结束时间:", time)
    print("状态:", state)
    print("价格:", price.strip())
    print("报名人数:", apply)
    print("提醒人数:", remind)
    print("围观人数:", surround)



