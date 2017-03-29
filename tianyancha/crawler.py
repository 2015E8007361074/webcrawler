# coding:utf-8
"""
create on Mar 29, 2017 By Wenyan Yu

该程序主要是实现从天眼查中提取指定公司的股东信息。思路如下:

1.用户给定公司名称(该公司名唯一存在)
2.通过搜索框搜索公司名称,进入公司搜索列表页面
3.根据用户给定的公司名称精确匹配列表项,并获取公司详细页面的URL
4.从公司详细页面的URL中获取提取公司的股东信息
"""
from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
import time


class Crawler(object):
    """爬虫类,爬取天眼查网站的信息"""
    def __init__(self, company_name):
        self.company_name = company_name # 初始化公司的名称

    def get_page_url(self):
        """根据公司名称获取搜索列表页面,并返回公司详细页面的URL"""
        self.company_name = self.company_name.encode('utf-8')
        search_list_url = "http://www.tianyancha.com/search?key="+quote(self.company_name)
        # print(search_list_url)
        try:
            # 为提高速度禁止加载图片
            driver = webdriver.PhantomJS(executable_path='/Users/wayne/Documents/Code/webcrawler/tianyancha/phantomjs',
                                         service_args=['--load-images=no'])
            driver.get(search_list_url)
            time.sleep(3)  # 延时等待页面加载
            page_source = driver.page_source
            bsObj = BeautifulSoup(page_source,"html.parser")
            bsObj = bsObj.find("div", {"class": "col-xs-10 search_repadding2 f18"})
            get_url = bsObj.find("a").attrs['href']
            get_company_name = bsObj.find("span").get_text()
            print("公司名称:",get_company_name)
            print("公司详细页面url:",get_url)
            if get_url is not None and (get_company_name.encode('utf-8') == self.company_name):
                return get_url
        except (AttributeError,HTTPError,URLError) as e:
            return None
        finally:
            driver.close()
        return None

    def get_page_info(self):
        """根据详细页面url,抓取公司详细页面中的股东信息"""
        page_url = self.get_page_url()
        shareholer_info_list = []
        if page_url is None:
            print("获取公司详细页面url失败!")
            return None
        else:
            try:
                # print(page_url)
                # 为提高速度,禁止加载图片
                driver = webdriver.PhantomJS(
                    executable_path='/Users/wayne/Documents/Code/webcrawler/tianyancha/phantomjs',
                                                                service_args=['--load-images=no'])
                driver.get(page_url)
                time.sleep(5)  # 延时等待页面加载
                page_source = driver.page_source
                bsObj = BeautifulSoup(page_source,"html.parser")
                tr_list = bsObj.find("table",{"class":"table companyInfo-table"}).find("tbody").findAll("tr")
                for tr_item in tr_list:
                    shareholer_info =[]
                    shareholer_info.append(tr_item.find("a").get_text())
                    shareholer_info.append(tr_item.findAll("span")[0].get_text())
                    shareholer_info.append(tr_item.findAll("span")[1].get_text())
                    shareholer_info_list.append(shareholer_info)
            except (AttributeError, HTTPError, URLError) as e:
                print("获取公司股东信息失败!")
                return None
            finally:
                driver.close()
            return shareholer_info_list

if __name__ == "__main__":
    # company_name = "深圳市腾讯计算机系统有限公司"
    # company_name = "北京百度网讯科技有限公司"
    company_name = "北京新浪互联信息服务有限公司"
    my_crawler = Crawler(company_name)
    shareholer_info_list = my_crawler.get_page_info()
    print("公司股东信息如下:股东 出资比例 认缴出资")
    for info in shareholer_info_list:
        for item in info:
            print(item,"  ", end='')
        print() # 换行