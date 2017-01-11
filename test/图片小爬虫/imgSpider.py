# coding=utf-8
# 百度贴吧图片网络小爬虫
"""
import re
import urllib


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getImg(html):
    reg = r'src="(.+?\.jpg)" '

    #正则表达式
    reg_s = r'src="(.+?\.jpg)" '
    imgre = re.compile(reg_s)
    imglist = imgre.findall(html)
    x = 0
    l = len(imglist)
    print "总共有%d张图片" % (l)
    print "- - - - - - - - - - - -"
    for imgurl in imglist:
        print "第%d张图片" % (x + 1)
        urllib.urlretrieve(imgurl, '.\\picture\\%s.jpg' % x)
        x = x + 1


html = getHtml("http://tieba.baidu.com/p/4421444969")
"""
# getImg(html)

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import os

defalut_directory = "picture"

def get_img(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return "链接访问失败！请检查网络链接。"
    try:
        bs_obj = BeautifulSoup(html, "html.parser")
        for link in bs_obj.findAll("img", {"class":"BDE_Image"}):
            if link.attrs['src'] is not None:
                print(link.attrs['src'].split("/")[-1])
                try:
                    urlretrieve(link.attrs['src'], "picture/"+link.attrs['src'].split("/")[-1])
                except FileNotFoundError as e:
                    os.makedirs("picture")
    except ValueError as e:
        return "页面信息获取异常！"
    return "图片信息获取成功！"

print(get_img("http://tieba.baidu.com/p/4906870997"))



