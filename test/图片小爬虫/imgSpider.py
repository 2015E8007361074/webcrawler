# coding=utf-8
# 百度贴吧图片网络小爬虫
#
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
getImg(html)
