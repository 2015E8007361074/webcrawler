# coding:utf-8
"""
create on Jan 5,2017 By Wenyan Yu

该程序是前面程序的重构代码，目的在于重构爬虫以爬去拍卖网上的拍卖商品详细信息：

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
2.所有采集到的拍买商品详细信息，保存为goods_info.csv文档，格式为：
标题，结束时间，拍卖状态，成交价格，报名人数，提醒人数，围观次数，起拍价，加价幅度，保证金，佣金，延时周期，保留价，送拍机构，特色服务
"""
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import csv
import json
import os


class Crawler(object):
    """爬虫类，用于爬去拍卖网站上的商品信息"""
    def __init__(self, calendar_list):
        self.calendar_list = calendar_list
        self.run_crawler()
        # self.url_for_per_day = "https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"
        # 上面是016年1月1日拍卖商品的列表页面
        # self.url = "https://sf.taobao.com/sf_item/525351764416.htm?spm=a213w.7398552.paiList.1.YEOjaL" # 拍卖结束，流拍
        # self.url = "https://sf.taobao.com/sf_item/541714260036.htm?spm=a213w.7398552.paiList.5.3YWi2H" # 拍卖结束，已成交
        # self.url = "https://sf.taobao.com/sf_item/541629168048.htm?spm=a213w.7398552.paiList.1.3YWi2H" # 正在进行的拍卖
        # self.url = "https://sf.taobao.com/sf_item/543245084757.htm?spm=a213w.7398552.paiList.4.BmB61J" # 被中止的拍卖
        # self.url = "https://sf.taobao.com/sf_item/543239404828.htm?spm=a213w.7398552.paiList.12.BmB61J" # 被撤回的拍卖

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
            bsObj = BeautifulSoup(html.read())
            # print(bsObj)
            # title = bsObj.find("h1").get_text().strip()
            title = "".join(bsObj.find("h1").get_text().split()) # 去除标题中的空格，换行符，制表符
            print("1.标题：", title)
            page_info.append(title)

            time = bsObj.find("span", {"class": "countdown J_TimeLeft"}).get_text()
            print("2.结束时间：", time)
            page_info.append(time)

            state = bsObj.find("span", {"class": "title"}).get_text()
            if state == "成交价":
                state = "已成交"
            else:
                state = "流拍"
            # 此处只针对历史拍卖记录进行抓取，所以不考虑正在进行的拍卖
            # 而有价格状态记录的信息有两种已成交和流拍的，对于撤回和终止的拍卖商品自动舍弃
            print("3.拍卖状态：", state)
            page_info.append(state)

            price = bsObj.find("span", {"class": "pm-current-price J_Price"}).get_text().strip()
            print("4.拍卖价格：", price)
            page_info.append(price)

            apply = bsObj.find("em", {"class": "J_Applyer"}).get_text().strip()
            print("5.报名人数：", apply)
            page_info.append(apply)

            remind = bsObj.find("span", {"class": "pm-reminder i-b"}).find("em").get_text().strip()
            print("6.提醒人数：", remind)
            page_info.append(remind)

            surround = bsObj.find("em", {"id": "J_Looker"}).get_text().strip()
            print("7.围观次数：", surround)
            page_info.append(surround)

            start_price = bsObj.find("tbody", {"id": "J_HoverShow"}).findAll("span",{"class":"J_Price"})[0].get_text().strip()
            print("8.起拍价：", start_price)
            page_info.append(start_price)

            increase_range = bsObj.find("tbody",{"id":"J_HoverShow"}).findAll("span",{"class":"J_Price"})[1].get_text().strip()
            print("9.加价幅度：", increase_range)
            page_info.append(increase_range)

            guarantee = bsObj.find("tbody",{"id": "J_HoverShow"}).findAll("span",{"class":"J_Price"})[3].get_text().strip()
            print("10.保证金：", guarantee)
            page_info.append(guarantee)

            charges = "无"
            print("11.佣金：", charges)
            page_info.append(charges)

            delay_period = bsObj.find("tbody", {"id": "J_HoverShow"}).find("td", {"class": "delay-td"}).findAll("span")[1].get_text().strip(": ")
            print("12.延时周期：", delay_period)
            page_info.append(delay_period)

            reserve_price = bsObj.find("tbody", {"id": "J_HoverShow"}).find("td", {"class": "reserve-td"}).findAll("span")[1].get_text().strip(": ")
            print("13.保留价：", reserve_price)
            page_info.append(reserve_price)

            insitution = "无"
            print("14.送拍机构：", insitution)
            page_info.append(insitution)

            special_service = "无"
            print("15.特色服务：", special_service)
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
            bsObj = BeautifulSoup(html)
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
            bsObj = BeautifulSoup(html)
            for list_data in bsObj.findAll("script", {"id": "sf-item-list-data"}):
                links = list_data.get_text()
                links_json = json.loads(links)
                # print(links_json)
                """
                输出json格式如下：
                {'data': [{'end': 1451718000000, 'timeToEnd': -31880535098, 'start': 1451631600000, 'viewerCount': 2105, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i4/TB1L6kKKVXXXXXzXpXX8GID8VXX', 'status': 'failure', 'delayCount': 0, 'title': '安龙县新安镇杨柳街1幢2单元6楼2号砖混房屋一套', 'initialPrice': 209851.7, 'applyCount': 1, 'xmppVersion': '2', 'id': 525351764416, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525351764416.htm', 'consultPrice': 209851.7, 'bidCount': 0, 'timeToStart': -31966935098, 'currentPrice': 209851.7}, {'end': 1451703192000, 'timeToEnd': -31895343098, 'start': 1451613600000, 'viewerCount': 2482, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1ha2tLXXXXXcMXFXX5pGJFXXX', 'status': 'done', 'delayCount': 15, 'title': '建德市寿昌镇东昌北路90号住宅房产', 'initialPrice': 720000.0, 'applyCount': 3, 'xmppVersion': '34', 'id': 525352044663, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525352044663.htm', 'consultPrice': 1112000.0, 'bidCount': 28, 'timeToStart': -31984935098, 'currentPrice': 720000.0}, {'end': 1451702392000, 'timeToEnd': -31896143098, 'start': 1451613600000, 'viewerCount': 6416, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i4/TB1W7oXKVXXXXbwXFXXgNdv.pXX', 'status': 'done', 'delayCount': 11, 'title': '杭州市西湖区金海公寓3幢4单元601室房屋', 'initialPrice': 1115000.0, 'applyCount': 9, 'xmppVersion': '57', 'id': 525293273999, 'supportLoans': 1, 'itemUrl': '//sf.taobao.com/sf_item/525293273999.htm', 'consultPrice': 1370000.0, 'bidCount': 53, 'timeToStart': -31984935098, 'currentPrice': 1115000.0}, {'end': 1451702111000, 'timeToEnd': -31896424098, 'start': 1451613600000, 'viewerCount': 5321, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i2/TB1zKQIKVXXXXcQXpXXnTVc.VXX', 'status': 'done', 'delayCount': 9, 'title': '大亚湾西区石化大道中512号星河半岛花园3栋17层06号房产', 'initialPrice': 390440.0, 'applyCount': 5, 'xmppVersion': '38', 'id': 525309391444, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525309391444.htm', 'consultPrice': 460050.0, 'bidCount': 29, 'timeToStart': -31984935098, 'currentPrice': 390440.0}, {'end': 1451702031000, 'timeToEnd': -31896504098, 'start': 1451613600000, 'viewerCount': 4107, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB11kwlKVXXXXboXVXXwbG98VXX', 'status': 'done', 'delayCount': 9, 'title': '新安江街道环城北路?金地家园3幢1-502室住宅房地产', 'initialPrice': 1300000.0, 'applyCount': 6, 'xmppVersion': '43', 'id': 525333982706, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525333982706.htm', 'consultPrice': 1789474.0, 'bidCount': 39, 'timeToStart': -31984935098, 'currentPrice': 1300000.0}, {'end': 1451701657000, 'timeToEnd': -31896878098, 'start': 1451613600000, 'viewerCount': 3134, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1WowlKVXXXXX3XFXX9Sjl9VXX', 'status': 'done', 'delayCount': 7, 'title': '泗阳县盛世嘉园15幢604室住宅房地产及装潢（含车库、阁楼）', 'initialPrice': 411720.0, 'applyCount': 5, 'xmppVersion': '32', 'id': 525321260310, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525321260310.htm', 'consultPrice': 450900.0, 'bidCount': 29, 'timeToStart': -31984935098, 'currentPrice': 411720.0}, {'end': 1451701487000, 'timeToEnd': -31897048098, 'start': 1451613600000, 'viewerCount': 4547, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1.tnpLXXXXXcmXVXXemZm8XXX', 'status': 'done', 'delayCount': 6, 'title': '杭州市西湖区城北商贸园22幢1单元302室', 'initialPrice': 924880.0, 'applyCount': 2, 'xmppVersion': '32', 'id': 525307514043, 'supportLoans': 1, 'itemUrl': '//sf.taobao.com/sf_item/525307514043.htm', 'consultPrice': 1380000.0, 'bidCount': 24, 'timeToStart': -31984935098, 'currentPrice': 924880.0}, {'end': 1451701097000, 'timeToEnd': -31897438098, 'start': 1451613600000, 'viewerCount': 2947, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i2/TB1eGZKKVXXXXXzXpXXGPdR8VXX', 'status': 'done', 'delayCount': 5, 'title': '建德市半岛国际1602、1603、1605、1606室房地产', 'initialPrice': 1200000.0, 'applyCount': 4, 'xmppVersion': '27', 'id': 525300827808, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525300827808.htm', 'consultPrice': 1666400.0, 'bidCount': 24, 'timeToStart': -31984935098, 'currentPrice': 1200000.0}, {'end': 1451701009000, 'timeToEnd': -31897526098, 'start': 1451613600000, 'viewerCount': 6515, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1m2sEKVXXXXX_XXXXs.yQ.XXX', 'status': 'done', 'delayCount': 5, 'title': '莆田市荔城区学园路北街108号锦峰龙园公寓1907号的房地产', 'initialPrice': 965000.0, 'applyCount': 10, 'xmppVersion': '46', 'id': 525324772257, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525324772257.htm', 'consultPrice': 1112700.0, 'bidCount': 43, 'timeToStart': -31984935098, 'currentPrice': 965000.0}, {'end': 1451700890000, 'timeToEnd': -31897645098, 'start': 1451613600000, 'viewerCount': 4075, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1FNKWLXXXXXbIXVXXTEQo.XXX', 'status': 'done', 'delayCount': 4, 'title': '连云港市海州区朝阳西路与江化路交叉口一宗工业国有出让建设用地', 'initialPrice': 2300000.0, 'applyCount': 3, 'xmppVersion': '19', 'id': 525258435673, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525258435673.htm', 'consultPrice': 1590000.0, 'bidCount': 12, 'timeToStart': -31984935098, 'currentPrice': 2300000.0}, {'end': 1451700829000, 'timeToEnd': -31897706098, 'start': 1451613600000, 'viewerCount': 8852, 'buyRestrictions': 1, 'picUrl': '//img.alicdn.com/bao/uploaded/i4/TB1ofDSKVXXXXX1aXXX97DR8pXX', 'status': 'done', 'delayCount': 4, 'title': '福州市仓山区上雁路56号金山碧水冬馨苑10#楼601复式单元', 'initialPrice': 1750000.0, 'applyCount': 14, 'xmppVersion': '42', 'id': 525267981469, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525267981469.htm', 'consultPrice': 1971200.0, 'bidCount': 39, 'timeToStart': -31984935098, 'currentPrice': 1750000.0}, {'end': 1451700801000, 'timeToEnd': -31897734098, 'start': 1451613600000, 'viewerCount': 6653, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i4/TB121QoKVXXXXXDXFXX6Q2N.XXX', 'status': 'done', 'delayCount': 4, 'title': '杭州市世纪新城26幢2单元402室房屋', 'initialPrice': 3430000.0, 'applyCount': 8, 'xmppVersion': '73', 'id': 525309625567, 'supportLoans': 1, 'itemUrl': '//sf.taobao.com/sf_item/525309625567.htm', 'consultPrice': 3331600.0, 'bidCount': 68, 'timeToStart': -31984935098, 'currentPrice': 3430000.0}, {'end': 1451700725000, 'timeToEnd': -31897810098, 'start': 1451613600000, 'viewerCount': 5585, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i3/TB10HY_KVXXXXXTXVXXh7fV.XXX', 'status': 'done', 'delayCount': 3, 'title': '杭州市下城区朝晖四小区54幢3单元702室房屋', 'initialPrice': 990000.0, 'applyCount': 3, 'xmppVersion': '11', 'id': 525307756717, 'supportLoans': 1, 'itemUrl': '//sf.taobao.com/sf_item/525307756717.htm', 'consultPrice': 1280000.0, 'bidCount': 7, 'timeToStart': -31984935098, 'currentPrice': 990000.0}, {'end': 1451700664000, 'timeToEnd': -31897871098, 'start': 1451613600000, 'viewerCount': 2402, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1o.UpKVXXXXcSXXXXST...XXX', 'status': 'done', 'delayCount': 3, 'title': '绍兴市越城区君悦大厦2208室房产（含室内固定装饰装修）', 'initialPrice': 466880.0, 'applyCount': 3, 'xmppVersion': '16', 'id': 525293625282, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525293625282.htm', 'consultPrice': 553600.0, 'bidCount': 12, 'timeToStart': -31984935098, 'currentPrice': 466880.0}, {'end': 1451700296000, 'timeToEnd': -31898239098, 'start': 1451613600000, 'viewerCount': 4417, 'buyRestrictions': 0, 'picUrl': '//img.alicdn.com/bao/uploaded/i1/TB1HgwkKVXXXXalXVXXFkKd.XXX', 'status': 'done', 'delayCount': 1, 'title': '徐州市中新.泉山森林海（一期）-1、YF29-4-402房产', 'initialPrice': 371200.0, 'applyCount': 9, 'xmppVersion': '23', 'id': 525291531299, 'supportLoans': 0, 'itemUrl': '//sf.taobao.com/sf_item/525291531299.htm', 'consultPrice': 479000.0, 'bidCount': 17, 'timeToStart': -31984935098, 'currentPrice': 371200.0}]}
                """
                for item in links_json["data"]:
                    print("https:"+item["itemUrl"])
                    links_per_page.append("https:"+item["itemUrl"])
        except (AttributeError, TypeError) as e:
            return None
        return links_per_page

    def get_links_per_day(self, day_url):
        """
        获取某一天所有拍卖商品的详细页面链接
        :param day_url:
        :return: links_per_day
        """
        url = day_url
        links_per_day = []
        if self.get_links_per_page(url) is None:
            print("网络连接失败，请检查网络连接是否正确！")
        while(self.get_next_page(url)):
            links_per_day.extend(self.get_links_per_page(url))
            url = self.get_next_page(url)
        return links_per_day

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
        给定某一天的拍卖商品列表页面，获取该天所有的拍卖商品详细信息并，存储到page_info_per_day.csv文件中
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

    def run_crawler(self):
        """根据需求开始爬取符合要求的数据，并将数据存储到csv文件中"""
        # print(self.calendar_list)
        links_list = [] # 存储指定日期内所有的拍卖商品详细页面的链接
        # 首先获取每一天的拍卖商品列表的首页面URL
        for link_per_day in self.calendar_list:
            # print(link_per_day)
            # 获取当天所有的拍卖商品详细页面的URL，并添加到link_list列表中
            links_list.extend(self.get_links_per_day(link_per_day))
        # 将制定日期内的所有拍卖商品的信息页面的链接存储到links.csv文件中
        self.store_links_to_file(links_list, "../data/links.csv")

        # 获取每一件拍卖商品详细页面的URL,并抽取页面中的拍卖商品的详细信息，添加到page_info_list列表中
        page_info_list = []
        for link in links_list:
            page_info = self.get_page_info(link)
            # print(page_info)
            if page_info is not None:
                page_info_list.append(page_info)

        # 将page_info_list拍卖商品详细信息存储到page_info.csv文件中
        self.store_page_info_to_csv(page_info_list, "../data/page_info.csv")

if __name__ == "__main__":
    # my_calendar_list 存储的是从2016年1月1日开始，每天拍卖商品列表的首页面
    """
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
    my_calendar_list = [
        "https://sf.taobao.com/calendar.htm?category=0&city=&tradeType=-1&province=&selectDate=1451577600000"
                       ]
    # 开始实例化爬虫类，并传入需要采集拍卖商品列表的日期链接，运行爬虫采集数据，每一天对应一个URL
    my_crawler = Crawler(my_calendar_list)

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
