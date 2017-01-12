# coding:utf-8
"""
create on Jan 5,2017 By Wenyan Yu

该程序是前面程序的重构代码，目的在于重构爬虫以爬取拍卖网上的拍卖商品详细信息：

根据那个不规范的需求文档，本程序需要实现以下功能：
1.保存商品详细页面的原始HTML代码
2.抽取拍卖商品的详细信息保存为csv格式，具体需要抽取的信息如此下：

1.标题
2.结束时间
3.拍卖状态（已成交/流拍） 注：对于撤回和终止的拍卖商品，由于没有相关信息，对采集到页面予以舍弃，不进行抽取
4.成交价格
5.报名人数
6.提醒人数
7.围观次数
8.起拍价
9.加价幅度
10.保证金
11.佣金（没找到，默认为无）
12.延时周期
13.保留价（有或无）
14.送拍机构（没找到默认为无）
15.特色服务（没找到，默认为无）

最后需要生成三个部分的信息：
1.所有详细页面的链接，保存为links.csv文档，格式为url,标题
2.所有采集到的拍买商品详细信息，保存为page_info.csv文档，格式为：
标题，结束时间，拍卖状态，成交价格，报名人数，提醒人数，围观次数，起拍价，加价幅度，保证金，佣金，延时周期，保留价，送拍机构，特色服务
"""
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import csv
import json
import os
import datetime
import time
import _thread


class Crawler(object):
    """爬虫类，用于爬去拍卖网站上的商品信息"""
    def __init__(self, start_time_epoch, end_time_epoch ):

        self.links_list = []  # 存储指定日期内所有的拍卖商品详细页面的链接
        self.page_info_list = [["标题",
                           "结束时间",
                           "拍卖状态",
                           "成交价格",
                           "报名人数",
                           "提醒人数",
                           "围观次数",
                           "起拍价",
                           "加价幅度",
                           "保证金",
                           "佣金",
                           "延时周期",
                           "保留价",
                           "送拍机构",
                           "特色服务"]]  # 存储所有采集到所有拍卖商品的详细信息
        self.start = start_time_epoch # 开始采集的时间
        self.end = end_time_epoch    # 结束采集的时间
        # 获取给定时间段拍卖商品的日历链接
        self.calendar_list = self.get_calendar_links(self.start, self.end)
        # 将获取到拍卖商品日历链接存储到calendar_links.csv当中
        self.store_links_to_file(self.calendar_list, "../data/calendar_links.csv")
        self.run_crawler()

    def get_page_info(self, url):
        """
        抓取商品详细信息，一共需抓取15项：
        标题，结束时间，拍卖状态，成交价格，报名人数，提醒人数，围观次数，起拍价，加价幅度，保证金，佣金，延时周期，保留价，送拍机构，特色服务
        :return: page_info
        """
        page_info = []
        try:
            html = urlopen(url)
        except (HTTPError, URLError) as e:
            return None

        try:
            bsObj = BeautifulSoup(html.read(),"html.parser")
            # print(bsObj)
            # title = bsObj.find("h1").get_text().strip()
            title = "".join(bsObj.find("h1").get_text().split()) # 去除标题中的空格，换行符，制表符
            # print("1.标题：", title)
            page_info.append(title)

            time = bsObj.find("span", {"class": "countdown J_TimeLeft"}).get_text()
            # print("2.结束时间：", time)
            page_info.append(time)

            state = bsObj.find("span", {"class": "title"}).get_text()
            if state == "成交价":
                state = "已成交"
            else:
                state = "流拍"
            # 此处只针对历史拍卖记录进行抓取，所以不考虑正在进行的拍卖
            # 而有价格状态记录的信息有两种已成交和流拍的，对于撤回和终止的拍卖商品自动舍弃
            # print("3.拍卖状态：", state)
            page_info.append(state)

            price = bsObj.find("span", {"class": "pm-current-price J_Price"}).get_text().strip()
            # print("4.拍卖价格：", price)
            page_info.append(price)

            apply = bsObj.find("em", {"class": "J_Applyer"}).get_text().strip()
            # print("5.报名人数：", apply)
            page_info.append(apply)

            remind = bsObj.find("span", {"class": "pm-reminder i-b"}).find("em").get_text().strip()
            # print("6.提醒人数：", remind)
            page_info.append(remind)

            surround = bsObj.find("em", {"id": "J_Looker"}).get_text().strip()
            # print("7.围观次数：", surround)
            page_info.append(surround)

            start_price = bsObj.find("tbody", {"id": "J_HoverShow"}).findAll("span",{"class":"J_Price"})[0].get_text().strip()
            # print("8.起拍价：", start_price)
            page_info.append(start_price)

            increase_range = bsObj.find("tbody",{"id":"J_HoverShow"}).findAll("span",{"class":"J_Price"})[1].get_text().strip()
            # print("9.加价幅度：", increase_range)
            page_info.append(increase_range)

            guarantee = bsObj.find("tbody",{"id": "J_HoverShow"}).findAll("span",{"class":"J_Price"})[3].get_text().strip()
            # print("10.保证金：", guarantee)
            page_info.append(guarantee)

            charges = "无"
            # print("11.佣金：", charges)
            page_info.append(charges)

            delay_period = bsObj.find("tbody", {"id": "J_HoverShow"}).find("td", {"class": "delay-td"}).findAll("span")[1].get_text().strip(": ")
            # print("12.延时周期：", delay_period)
            page_info.append(delay_period)

            reserve_price = bsObj.find("tbody", {"id": "J_HoverShow"}).find("td", {"class": "reserve-td"}).findAll("span")[1].get_text().strip(": ")
            # print("13.保留价：", reserve_price)
            page_info.append(reserve_price)

            insitution = "无"
            # print("14.送拍机构：", insitution)
            page_info.append(insitution)

            special_service = "无"
            # print("15.特色服务：", special_service)
            page_info.append(special_service)

            # for child in bsObj.find("tbody", {"id": "J_HoverShow"}).children:
            #    print(child)
            # print(bsObj.find("tbody",{"id":"J_HoverShow"}).findAll("span",{"class":"J_Price"}))

        except (AttributeError, IndexError) as e:
            return None
        return page_info

    def get_next_page(self, pre_url):
        """获取下一个分页的URL"""
        try:
            html = urlopen(pre_url)
        except (HTTPError, URLError) as e:
            return None
        try:
            bsObj = BeautifulSoup(html, "html.parser")
            for link in bsObj.findAll("span", {"class": "next unavailable"}):
                if link is not None:
                    return None
        except AttributeError as e:
            return None
        finally:
            for link in bsObj.findAll("a",{"class": "next"}):
                next_page = "https:"+link.attrs['href'].strip()
        return next_page

    def get_links_per_page(self, page_url):
        """
        获取一个页面中的全部拍卖商品的详细页面链接
        :return links_per_page
        """
        links_per_page = []
        try:
            html = urlopen(page_url)
        except (HTTPError, URLError) as e:
            return None
        try:
            bsObj = BeautifulSoup(html, "html.parser")
            for list_data in bsObj.findAll("script", {"id": "sf-item-list-data"}):
                links = list_data.get_text()
                links_json = json.loads(links)
                # print(links_json)
                """
                输出json格式如下：
                {'data': [{'end': 1451718000000, 'timeToEnd': -31880535098, 'start': 1451631600000, 'viewerCount': 2105, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i4/TB1L6kKKVXXXXXzXpXX8GID8VXX', 'status': 'failure', 'delayCount': 0, 'title': '安龙县新安镇杨柳街1幢2单元6楼2号砖混房屋一套', 'initialPrice': 209851.7, 'applyCount': 1, 'xmppVersion': '2', 'id': 525351764416, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525351764416.htm', 'consultPrice': 209851.7, 'bidCount': 0, 'timeToStart': -31966935098, 'currentPrice': 209851.7}, {'end': 1451703192000, 'timeToEnd': -31895343098, 'start': 1451613600000, 'viewerCount': 2482, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1ha2tLXXXXXcMXFXX5pGJFXXX', 'status': 'done', 'delayCount': 15, 'title': '建德市寿昌镇东昌北路90号住宅房产', 'initialPrice': 720000.0, 'applyCount': 3, 'xmppVersion': '34', 'id': 525352044663, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525352044663.htm', 'consultPrice': 1112000.0, 'bidCount': 28, 'timeToStart': -31984935098, 'currentPrice': 720000.0}, {'end': 1451702392000, 'timeToEnd': -31896143098, 'start': 1451613600000, 'viewerCount': 6416, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i4/TB1W7oXKVXXXXbwXFXXgNdv.pXX', 'status': 'done', 'delayCount': 11, 'title': '杭州市西湖区金海公寓3幢4单元601室房屋', 'initialPrice': 1115000.0, 'applyCount': 9, 'xmppVersion': '57', 'id': 525293273999, 'supportLoans': 1, 'itemUrl': '//sf.taobao.com/sf_item/525293273999.htm', 'consultPrice': 1370000.0, 'bidCount': 53, 'timeToStart': -31984935098, 'currentPrice': 1115000.0}, {'end': 1451702111000, 'timeToEnd': -31896424098, 'start': 1451613600000, 'viewerCount': 5321, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i2/TB1zKQIKVXXXXcQXpXXnTVc.VXX', 'status': 'done', 'delayCount': 9, 'title': '大亚湾西区石化大道中512号星河半岛花园3栋17层06号房产', 'initialPrice': 390440.0, 'applyCount': 5, 'xmppVersion': '38', 'id': 525309391444, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525309391444.htm', 'consultPrice': 460050.0, 'bidCount': 29, 'timeToStart': -31984935098, 'currentPrice': 390440.0}, {'end': 1451702031000, 'timeToEnd': -31896504098, 'start': 1451613600000, 'viewerCount': 4107, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB11kwlKVXXXXboXVXXwbG98VXX', 'status': 'done', 'delayCount': 9, 'title': '新安江街道环城北路?金地家园3幢1-502室住宅房地产', 'initialPrice': 1300000.0, 'applyCount': 6, 'xmppVersion': '43', 'id': 525333982706, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525333982706.htm', 'consultPrice': 1789474.0, 'bidCount': 39, 'timeToStart': -31984935098, 'currentPrice': 1300000.0}, {'end': 1451701657000, 'timeToEnd': -31896878098, 'start': 1451613600000, 'viewerCount': 3134, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1WowlKVXXXXX3XFXX9Sjl9VXX', 'status': 'done', 'delayCount': 7, 'title': '泗阳县盛世嘉园15幢604室住宅房地产及装潢（含车库、阁楼）', 'initialPrice': 411720.0, 'applyCount': 5, 'xmppVersion': '32', 'id': 525321260310, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525321260310.htm', 'consultPrice': 450900.0, 'bidCount': 29, 'timeToStart': -31984935098, 'currentPrice': 411720.0}, {'end': 1451701487000, 'timeToEnd': -31897048098, 'start': 1451613600000, 'viewerCount': 4547, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1.tnpLXXXXXcmXVXXemZm8XXX', 'status': 'done', 'delayCount': 6, 'title': '杭州市西湖区城北商贸园22幢1单元302室', 'initialPrice': 924880.0, 'applyCount': 2, 'xmppVersion': '32', 'id': 525307514043, 'supportLoans': 1, 'itemUrl': '//sf.taobao.com/sf_item/525307514043.htm', 'consultPrice': 1380000.0, 'bidCount': 24, 'timeToStart': -31984935098, 'currentPrice': 924880.0}, {'end': 1451701097000, 'timeToEnd': -31897438098, 'start': 1451613600000, 'viewerCount': 2947, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i2/TB1eGZKKVXXXXXzXpXXGPdR8VXX', 'status': 'done', 'delayCount': 5, 'title': '建德市半岛国际1602、1603、1605、1606室房地产', 'initialPrice': 1200000.0, 'applyCount': 4, 'xmppVersion': '27', 'id': 525300827808, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525300827808.htm', 'consultPrice': 1666400.0, 'bidCount': 24, 'timeToStart': -31984935098, 'currentPrice': 1200000.0}, {'end': 1451701009000, 'timeToEnd': -31897526098, 'start': 1451613600000, 'viewerCount': 6515, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1m2sEKVXXXXX_XXXXs.yQ.XXX', 'status': 'done', 'delayCount': 5, 'title': '莆田市荔城区学园路北街108号锦峰龙园公寓1907号的房地产', 'initialPrice': 965000.0, 'applyCount': 10, 'xmppVersion': '46', 'id': 525324772257, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525324772257.htm', 'consultPrice': 1112700.0, 'bidCount': 43, 'timeToStart': -31984935098, 'currentPrice': 965000.0}, {'end': 1451700890000, 'timeToEnd': -31897645098, 'start': 1451613600000, 'viewerCount': 4075, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1FNKWLXXXXXbIXVXXTEQo.XXX', 'status': 'done', 'delayCount': 4, 'title': '连云港市海州区朝阳西路与江化路交叉口一宗工业国有出让建设用地', 'initialPrice': 2300000.0, 'applyCount': 3, 'xmppVersion': '19', 'id': 525258435673, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525258435673.htm', 'consultPrice': 1590000.0, 'bidCount': 12, 'timeToStart': -31984935098, 'currentPrice': 2300000.0}, {'end': 1451700829000, 'timeToEnd': -31897706098, 'start': 1451613600000, 'viewerCount': 8852, 'buyRestrictions': 1, 'picUrl': '//img.alicdn.com/bao/uploaded/i4/TB1ofDSKVXXXXX1aXXX97DR8pXX', 'status': 'done', 'delayCount': 4, 'title': '福州市仓山区上雁路56号金山碧水冬馨苑10#楼601复式单元', 'initialPrice': 1750000.0, 'applyCount': 14, 'xmppVersion': '42', 'id': 525267981469, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525267981469.htm', 'consultPrice': 1971200.0, 'bidCount': 39, 'timeToStart': -31984935098, 'currentPrice': 1750000.0}, {'end': 1451700801000, 'timeToEnd': -31897734098, 'start': 1451613600000, 'viewerCount': 6653, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i4/TB121QoKVXXXXXDXFXX6Q2N.XXX', 'status': 'done', 'delayCount': 4, 'title': '杭州市世纪新城26幢2单元402室房屋', 'initialPrice': 3430000.0, 'applyCount': 8, 'xmppVersion': '73', 'id': 525309625567, 'supportLoans': 1, 'itemUrl': '//sf.taobao.com/sf_item/525309625567.htm', 'consultPrice': 3331600.0, 'bidCount': 68, 'timeToStart': -31984935098, 'currentPrice': 3430000.0}, {'end': 1451700725000, 'timeToEnd': -31897810098, 'start': 1451613600000, 'viewerCount': 5585, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i3/TB10HY_KVXXXXXTXVXXh7fV.XXX', 'status': 'done', 'delayCount': 3, 'title': '杭州市下城区朝晖四小区54幢3单元702室房屋', 'initialPrice': 990000.0, 'applyCount': 3, 'xmppVersion': '11', 'id': 525307756717, 'supportLoans': 1, 'itemUrl': '//sf.taobao.com/sf_item/525307756717.htm', 'consultPrice': 1280000.0, 'bidCount': 7, 'timeToStart': -31984935098, 'currentPrice': 990000.0}, {'end': 1451700664000, 'timeToEnd': -31897871098, 'start': 1451613600000, 'viewerCount': 2402, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1o.UpKVXXXXcSXXXXST...XXX', 'status': 'done', 'delayCount': 3, 'title': '绍兴市越城区君悦大厦2208室房产（含室内固定装饰装修）', 'initialPrice': 466880.0, 'applyCount': 3, 'xmppVersion': '16', 'id': 525293625282, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525293625282.htm', 'consultPrice': 553600.0, 'bidCount': 12, 'timeToStart': -31984935098, 'currentPrice': 466880.0}, {'end': 1451700296000, 'timeToEnd': -31898239098, 'start': 1451613600000, 'viewerCount': 4417, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1HgwkKVXXXXalXVXXFkKd.XXX', 'status': 'done', 'delayCount': 1, 'title': '徐州市中新.泉山森林海（一期）-1、YF29-4-402房产', 'initialPrice': 371200.0, 'applyCount': 9, 'xmppVersion': '23', 'id': 525291531299, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525291531299.htm', 'consultPrice': 479000.0, 'bidCount': 17, 'timeToStart': -31984935098, 'currentPrice': 371200.0}]}
                """
                for item in links_json["data"]:
                    # print("https:"+item["itemUrl"])
                    links_per_page.append("https:"+item["itemUrl"])
        except (AttributeError, TypeError) as e:
            return None
        return links_per_page

    def get_links_per_day(self, day_url, lock):
        """
        获取某一天所有拍卖商品的详细页面链接
        :param day_url:
        :return: links_per_day
        """
        print("开始新的线程,lock:", lock, "...")
        thread_start = time.time()
        url = day_url
        links_per_day = []
        if self.get_links_per_page(url) is None:
            print("网络连接失败，请检查网络连接是否正确！")
        while(self.get_next_page(url)):
            links_per_day.extend(self.get_links_per_page(url))
            url = self.get_next_page(url)
        self.links_list.extend(links_per_day) # 将获取的当天拍卖商品详细页面链接添加到links_list中
        thread_end = time.time()
        print("线程",lock,"运行结束，耗时：%s s" %(thread_end - thread_start))
        lock.release()
        # return links_per_day

    def store_links_to_file(self, res_list, des_path):
        """
        输入需要list格式的数据以及需要存储的文件路劲，将列表文件存储为csv格式
        :param res_list:
        :param des_path:
        :return: None
        """
        # print(os.getcwd())

        # print(res_list)
        """
        file_in = open(des_path, 'w+')

        try:
            # writer = csv.writer(csvFile)
            for i in res_list:
                print(i)
                file_in.write("".join(i))
        finally:
            file_in.close()
        """
        file = open(des_path, "w")
        try:
            for i in res_list:
                file.write(i+'\n')
        finally:
            file.close()

    def store_page_info_to_csv(self, res_list, des_path):
        """
        将拍卖商品详细信息列表中的数据存储到page_info_per_day.csv文件中
        :return:None
        """
        csvFile = open(des_path, 'w+', encoding='utf-8')
        try:
            writer = csv.writer(csvFile)
            for i in res_list:
                writer.writerow(i)
        except TypeError as e:
            print("The res_list is None!Please ensure the network is connected!")
        finally:
            csvFile.close()

    def get_calendar_links(self, start_time_epoch, end_time_epoch):
        """获取指定时间段的拍卖商品列表的日历链接"""
        calendar_links_list = []
        # print("开始时间戳：", start_time_epoch)
        # print("结束时间戳：", end_time_epoch)
        start = time.time()  # 运行开始
        print("正在获取商品列表日历链接...")
        if start_time_epoch > end_time_epoch:
            print("您输入的时间区间有有误，请重新输入！")
            return None

        while start_time_epoch <= end_time_epoch:
            current_time = start_time_epoch
            link = "https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=" + str(
                current_time) + "000"
            # print(link)
            calendar_links_list.append(link)
            start_time_epoch += 86400
        end = time.time()  # 运行结束
        print("商品列表日历链接获取完成,共%d条记录, time consuming:%d s" % (len(calendar_links_list), (end - start)))
        return calendar_links_list

    def multi_thread(self, calendar_list):
        """
        多线程获取所有拍卖商品详细页面的URL
        警告!
        为了方面，没有对并发线程做实际控制，以calendar_list的长度做并发线程数
        :param calendar_list: 日历链接列表multithreaded/mtsleepB.py:20
        :return: link_list　所有拍卖商品详细页面的URL
        """
        print("正在获取所有拍卖商品详细页面URL...")
        start = time.time()
        locks = []
        loops = range(len(calendar_list))
        # 创建锁列表
        for i in loops:
            lock = _thread.allocate_lock()
            lock.acquire()
            locks.append(lock)
        for i in loops:
            _thread.start_new_thread(self.get_links_per_day, (calendar_list[i], locks[i]))
        for i in loops:
            while locks[i].locked():pass
        end = time.time()
        print("拍卖商品详细页面URL获取完成,共%d条记录, time consuming:%d s" % (len(self.links_list), (end - start)))

    def run_crawler(self):
        """根据需求开始爬取符合要求的数据，并将数据存储到csv文件中"""
        # 多线程，首先获取每一天的拍卖商品列表的首页面URL
        self.multi_thread(self.calendar_list)
        # 将指定日期内的所有拍卖商品的信息页面的链接存储到links.csv文件中
        print("将指定日期内的所有拍卖商品的信息页面的链接存储到links.csv文件中")
        self.store_links_to_file(self.links_list, "../data/links.csv")

        # 获取每一件拍卖商品详细页面的URL,并抽取页面中的拍卖商品的详细信息，添加到page_info_list列表中
        print("正在获取所有指定日期内全部商品的详细信息...")
        start = time.time()
        for link in self.links_list:
            page_info = self.get_page_info(link)
            print("正在获取"+link+"页面信息...")
            # print(page_info)
            if page_info is not None:
                self.page_info_list.append(page_info)
        end = time.time()
        print("指定日期内全部拍卖商品详细信息获取完成,共%d条记录, time consuming:%d s, 平均每个页面抽取时间为%f s"
              % (len(self.page_info_list), (end - start), (end - start)/len(self.page_info_list)))

        # 将page_info_list拍卖商品详细信息存储到page_info.csv文件中
        print("将page_info_list拍卖商品详细信息存储到page_info.csv文件中")
        self.store_page_info_to_csv(self.page_info_list, "../data/page_info.csv")

if __name__ == "__main__":
    # 自动采集任意时间段内的功能已添加完毕

    run_start = time.time()  # 运行开始
    print("------------------开始采集---------------------------")
    # 开始采集的时间
    # 只需要填写年月日，如2016年1月1日->(2016,1,1,0,0,0)
    start_time = datetime.datetime(2016,2,1,0,0,0)
    # 结束采集的时间，要求同上
    end_time = datetime.datetime(2016,2,5,0,0,0)
    print("开始时间：", start_time)
    print("结束时间：", end_time)
    # 将时间格式转换为Unix时间戳
    start_time_epoch = round(time.mktime(start_time.timetuple()))
    end_time_epoch = round(time.mktime(end_time.timetuple()))
    # 开始实例化爬虫类
    # 传入开始采集和结束采集时间区间
    my_crawler = Crawler(start_time_epoch, end_time_epoch)

    run_end = time.time()  # 运行结束
    print("------------------结束采集---------------------------")
    print("time consuming:%d s" %(run_end-run_start))


    # print(my_crawler.get_page_info())
    # print(my_crawler.get_next_page("https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"))
    # print(my_crawler.get_links_per_page("https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"))
    # print(my_crawler.get_links_per_day("https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"))

    # 将某一天的所有拍卖商品的详细页面存储到links_per_day.csv
    """
    my_crawler.store_links_to_file(
        my_crawler.get_links_per_day("https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"),
            "../data/links_per_day.csv")
    """
    """
    my_crawler.store_page_info_to_csv(
        "https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000",
            "../data/page_info_per_day.csv")
    """

"""
关于并行爬虫的一些思考，考虑到在爬取数据是绝大部分的时间损耗都在网络延迟上
利用多线程爬取信息对速度的提升并不是很显著
因此还需要进一步研究
今天的研究就到这里吧

经测试：
串行爬取2016.1.8,2016.1.9,2016.1.10三天的全部拍卖商品详细链接共需284 s 或 134 s
并行爬取2016.1.8,2016.1.9,2016.1.10三天的全部拍卖商品详细链接共需144 s 或 89 s


串行爬取2016.2.1到2016.2.5　五天的全部拍卖商品详细链接共需 821 s
并行爬取2016.2.1到2016.2.5　五天的全部拍卖商品详细链接共需 191 s

具体需要多久没时间，每次运行的时间可能有所不一样，这个与当时的网络状态有关系
多测几次，求个平均值
大致也能看的出，并行爬取对爬取的速度有所提升，但是却不是很显著
因此需要分析程序的时间消耗到底在哪里,那些地方需要进一步改进
"""