# coding:utf-8
"""
create on Jan 11,2017 by Wenyan Yu

该程序用来下载页面文件，但是暂没对文件进行检查, 因此有安全隐患

请谨慎运行！！！
"""
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os

download_dir = "download"
base_url = "http://www.mryu.top"


def get_absolute_url(base_url, source):
    if source.startswith("http://wwww."):
        url = "http://"+source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = "http://"+source[4:]
    else:
        url = base_url+"/"+source

    """
    if base_url not in url:  # 剔除外链的干扰
        return None
    """
    return url


def get_download_path(base_url, absolute_url, download_dir):
    path = absolute_url.replace("wwww.", "")
    # path = path.replace(base_url, "")
    path = download_dir+path
    print(path.split("/"))
    # directory = os.path.dirname(path)
    # print(directory)

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if path.split("/")[-1] is None:
        return None
    else:
        return download_dir+"/"+path.split("/")[-1]


html = urlopen("http://www.mryu.top")
bs_obj = BeautifulSoup(html, "html.parser")
download_list = bs_obj.findAll(src=True)

for download in download_list:
    file_url = get_absolute_url(base_url, download["src"])
    if file_url is not None:
        print(file_url)
        urlretrieve(file_url, get_download_path(base_url, file_url, download_dir))
