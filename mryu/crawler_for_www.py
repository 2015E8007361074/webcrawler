# coding:utf-8
"""
create on Jan 10,2017 by Wenyan Yu

a small crawler to wwww
"""

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random
import os

random.seed(datetime.datetime.now())
print("当前时间：",datetime.datetime.now())


def get_internal_links(bsObj, url):
    """
    获取页面所有内链的列表
    :param bsObj:
    :param url:
    :return: internal_links
    """
    internal_links = []
    # help(urlparse)
    """
    urlparse
    Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    """
    domain = urlparse(url).scheme+"://"+urlparse(url).netloc  # 带scheme的domain
    # print(domain)
    # 找出所有以"/"开头的链接
    for link in bsObj.findAll("a", href=re.compile("^(/|.*"+domain+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                if link.attrs['href'].startswith('/'):
                    internal_links.append(domain+link.attrs['href'])
                else:
                    internal_links.append(link.attrs['href'])
    return internal_links


def get_external_links(bsObj, url):
    """
    获取页面所有的外链列表
    :param bsObj:
    :param url:
    :return:external_links
    """
    external_links = []
    domain = urlparse(url).netloc  # 不带scheme的domain
    # 找出所有以"http"或"www"开头，也不包含当前URL的链接
    for link in bsObj.findAll("a",
                              href=re.compile("^(http|www)((?!"+domain+").)*$")):
         if link.attrs['href'] is not None:
             if link.attrs['href'] not in external_links:
                 external_links.append(link.attrs['href'])
    return external_links


def get_random_external_link(url):
    """
    获取随机的外链
    :param url:
    :return:random_external_link
    """
    try:
        html = urlopen(url, timeout=1)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html, "html.parser")
        external_links = get_external_links(bsObj, url)
        # print("外链:", external_links)
        if len(external_links) == 0:
            print("该页面没有外链，获取该页面的内链")
            internal_links = get_internal_links(bsObj, url)
            # print(internal_links)
            internal_link = internal_links[random.randint(0, len(internal_links)-1)]
            print("该页面的随机内链：",internal_link)
            return get_random_external_link(internal_link)
        else:
            return external_links[random.randint(0, len(external_links)-1)]
    except (ValueError, TypeError) as e:
        return None


def follow_external_only(url):
    """
    利用递归，不断的输出随机外链，实现www任意页面的采集                      datetime.datetime.now()
    :param url:
    :return: None
    """
    external_link = get_random_external_link(url)
    if external_link is not None:
        print("当前随机外链是："+external_link)
        follow_external_only(external_link)
    else:
        print("程序终止！")
        return


def get_all_external_link(site_url):
    """采集网站的所有外链列表"""
    try:
        html = urlopen(site_url)
    except (HTTPError, URLError) as e:
        print("链接失败，请检查网络链接！")
        return None
    try:
        bsObj = BeautifulSoup(html, "html.parser")
        internal_links = get_internal_links(bsObj, site_url)
        external_links = get_external_links(bsObj, site_url)
        for link in external_links:
            if link not in all_ext_links:
                all_ext_links.add(link)
                print(link)
        for link in internal_links:
            if link not in all_int_links:
                # print("即将获取链接的URL是:"+link)
                all_int_links.add(link)
                get_all_external_link(link)
    except (ValueError, TypeError, NameError) as e:
        return None

if __name__ == "__main__":
    all_ext_links = set()
    all_int_links = set()

    start_page = "http://www.mryu.top/guest"
    # print(urlparse(start_page).netloc)
    site_url = "http://oreilly.com"
    # start_page = "http://oreilly.com"
    # follow_external_only(start_page)
    get_all_external_link(site_url)
    print("-------输出当前站点的全部外链到ext_link.csv中------------")
    print("正在写入...")
    file_out = open("ext_link_mryu.csv", "w+")
    try:
        for link in all_ext_links:
            file_out.write(link+'\n')
    finally:
        file_out.close()
    print("写入完成！")
    print("--------------------------------------------------------")