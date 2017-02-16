# coding:utf-8
"""
create on February 16. 2017 by Wayne
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string


def clean_input(n_input):
    """
    数据清理函数
    :param n_input:
    :return:
    """
    n_input = re.sub('\n+', " ", n_input)
    n_input = re.sub('\[[0-9]\]', "", n_input)
    n_input = re.sub(' +', " ", n_input)
    n_input = bytes(n_input, "UTF-8")
    n_input = n_input.decode("ascii", "ignore")
    print(n_input)
    n_input = n_input.strip().split(' ')  # 使用strip()函数去除字符串首尾两端的空格、换行等空白字符
    clean = []
    for item in n_input:
        item = item.strip(string.punctuation)  # string.punctuation 可以用来获取python的所有标点符号
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            clean.append(item)
    return clean


def n_grams(n_input, n):
    """
    n-grams 单词序列生成函数
    :param n_input:
    :param n:
    :return:
    """
    n_input = clean_input(n_input)
    output = []
    for i in range(len(n_input)-n+1):
        output.append(n_input[i:i+n])
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, "html.parser")
content = bsObj.find("div", {"id": "mw-content-text"}).get_text()

# n_grams = n_grams("i am wayne, what is your name ?", 2)
n_grams = n_grams(content, 2)
print(n_grams)
print("2_grams count is:"+str(len(n_grams)))