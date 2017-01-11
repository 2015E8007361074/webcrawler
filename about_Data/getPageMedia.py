# coding:utf-8
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com")
bs_obj = BeautifulSoup(html, "html.parser")
image_location = bs_obj.find("a", {"id":"logo"}).find("img")["src"]
urlretrieve(image_location, "download/logo.jpg")