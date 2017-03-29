from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
# Retrieve HTML string from the URL


def get_title(url):
    try:
        html=urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bsObj= BeautifulSoup(html.read())
        print(bsObj)
        title=bsObj.body.h1
    except AttributeError as e:
        return None
    return title

title = get_title("https://item-paimai.taobao.com/pmp_item/545246887011.htm")

if title == None:
    print("Title could not be found")
else:
    print(title)


