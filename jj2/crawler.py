# coding:utf-8
"""
create on Jan 22, 2018 By Wenyan Yu use python version 3.6
该程序主要是为了解决抓取淘宝拍卖网页面动态加载的问题
由于出价记录是动态加载的，因此采用常规的静态抓取无效，需要结合selenium+phantomjs实现动态抓取
页面的信息提取还是采用BeautifulSoup

示例地址：https://item-paimai.taobao.com/pmp_item/538916398974.htm?s=pmp_detail

抓取出价记录
竞拍人、价格、时间

经实验发现出价记录的抓取，问题不是出在页面动态加载的问题上

"""

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

page_url = "https://item-paimai.taobao.com/pmp_item/538916398974.htm?s=pmp_detail"

#为提高速度，禁止加载图片
# driver = webdriver.PhantomJS(
#     executable_path='/Users/wayne/Documents/Code/webcrawler/tianyancha/phantomjs',
#     service_args=['--load-images=no'])
# driver.get(page_url)
# time.sleep(0)  # 延时等待页面加载(单位为秒)
# page_source = driver.page_source
page_source = urlopen(page_url)
bsObj = BeautifulSoup(page_source, "html.parser")
# print(bsObj)

# <div class="record-list J_Content" data-from="/api/pmp/779328598974/bid-list" data-spm="6861993" id="J_RecordList">
data_from = bsObj.find("div", {"class": "record-list J_Content"})['data-from']
print("data-from:", data_from)
api_url = "https://item-paimai.taobao.com" + data_from
print("api-url：", api_url)
html = urlopen(api_url)
hjson = json.loads(html.read())
print(hjson)
print("第1页")
for item in hjson['list']:
    bidder = item['bidBasic']['bidderNo']
    bid_price = item['bidBasic']['bidPrice']
    bid_price = bid_price//100
    bid_time = item['bidBasic']['bidTime']
    bid_type = item['bidBasic']['type']
    item_id = item['bidBasic']['itemId']
    # 将基秒转化成时间
    bid_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(bid_time//1000)))
    print(bidder, ',', bid_price, ',', bid_time, ',', bid_type, ',', item_id)

total_page = hjson["paging"]["totalPage"]
# print("total_page:", total_page)

if total_page > 1:
    for i in range(2,total_page+1):
        print("第", i, "页")
        api_url = "https://item-paimai.taobao.com" + data_from+"?currentPage=" + str(i)
        # print("api_url:", api_url)
        html = urlopen(api_url)
        hjson = json.loads(html.read())
        # print(hjson)
        for item in hjson['list']:
            bidder = item['bidBasic']['bidderNo']
            bid_price = item['bidBasic']['bidPrice']
            bid_price = bid_price // 100
            bid_time = item['bidBasic']['bidTime']
            bid_type = item['bidBasic']['type']
            item_id = item['bidBasic']['itemId']
            # 将基秒转化成时间
            bid_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(bid_time // 1000)))
            print(bidder, ',', bid_price, ',', bid_time, ',', bid_type, ',', item_id)

# tr_list = bsObj.find("table", {"class": "pm-record-list"}).find("tbody").findAll("tr")
# for tr_item in tr_list:
#     print(tr_item)
# driver.close()