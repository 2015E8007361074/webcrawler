# coding=utf-8
import urllib2
request = urllib2.Request("http://www.baidu.com")
response = urllib2.urlopen(request)

print response.read()

#爬了第一个网页了