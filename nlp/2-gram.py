# coding:utf-8
"""
create on February 16. 2017 by Wayne
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import OrderedDict  # OrderedDict可以解决Python中字典的无序问题


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
    n_input = n_input.upper()  # 大小写也会影响序列的统计
    """
    不加大小写的结果：2_grams count is:6608
    去除大小写的干扰：2_grams count is:6462
    """
    print(n_input)
    n_input = n_input.strip().split(' ')  # 使用strip()函数去除字符串首尾两端的空格、换行等空白字符

    clean = []
    for item in n_input:
        item = item.strip(string.punctuation)  # string.punctuation 可以用来获取python的所有标点符号
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            clean.append(item)
    return clean


def get_ngrams(n_input, n):
    """
    n-grams 单词序列生成函数
    :param n_input:
    :param n:
    :return:
    """
    n_input = clean_input(n_input)
    output = {}
    for i in range(len(n_input)-n+1):  # 此处的循环，利用Python字典的特性很好实现了词频的统计
        new_gram = " ".join(n_input[i:i+n])
        if new_gram in output:
            output[new_gram] += 1
        else:
            output[new_gram] = 1
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, "html.parser")
content = bsObj.find("div", {"id": "mw-content-text"}).get_text()

# n_grams = n_grams("i am wayne, what is your name ?", 2)
n_grams = get_ngrams(content, 2)
n_grams = OrderedDict(sorted(n_grams.items(), key=lambda t: t[1], reverse=True))
print(n_grams)
print("2_grams count is:"+str(len(n_grams)))