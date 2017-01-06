from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()


def get_links(page_url):
    global pages
    html = urlopen("http://www.taobao.com/")
    bs_obj = BeautifulSoup(html)
    for link in bs_obj.findAll("a"):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # This is a new page
                new_page = link.attrs['href']
                print(new_page)
                pages.add(new_page)
                get_links(new_page)
get_links("")
