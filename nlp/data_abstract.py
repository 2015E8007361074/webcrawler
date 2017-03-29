# coding:utf-8
"""
create on February 16. 2017 by Wayne
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import OrderedDict  # OrderedDict可以解决Python中字典的无序问题
import operator


def is_common(word):
    """
    判断
    :param word:
    :return:
    """
    common_words = ["the", "be", "and", "of", "a", "in", "to", "have", "it", "i", "that", "for", "you", "he", "with",
                   "on", "do", "say", "this", "they", "is", "an", "at", "but", "we", "his", "from", "that", "not", "by",
                   "she", "or", "as", "what", "go", "their", "can", "who", "get", "if", "would", "her", "all", "my",
                   "make", "about", "know", "will", "as", "up", "one", "time", "has", "been", "there", "year", "so",
                   "think", "when", "which", "them", "some", "me", "people", "take", "out", "into", "just", "see",
                   "him", "your", "come", "could", "now", "than", "like", "other", "how", "then", "its", "our", "two",
                   "more", "these", "want", "way", "look", "first", "also", "new", "because", "day", "more", "use",
                   "no", "man", "find", "here", "thing", "give", "many", "well"]
    if word in common_words:
        return True
    return False


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
    n_input = n_input.lower()  # 大小写也会影响序列的统计
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
            if not is_common(item):
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


def get_gram_sentence(gram, content):
    """
    根据主题词，查找文本的主题句
    :param gram:
    :param content:
    :return:
    """
    content = re.sub("\n", " ", content)
    content = re.sub("\[[0-9]\]", "", content)
    content = re.sub(" +", " ", content)
    # print(content)
    sentences = content.split(".")
    # print(sentences)
    for sentence in sentences:
        if gram in sentence.lower().strip():
            # theme.append(sentence)
            return sentence.strip()+"."
    return ""


def get_theme(n_grams, N, content):
    """
    根据n_grams生成的主题词排名信息，获取文本的主题句
    n_grams表示主题词排名信息
    N代表前N个主题词，也就是表示要抽取N个主题句
    content表示
    :param n_grams:
    :param N:
    :param content:
    :return:
    """
    grams = []  # 存储前N个主题词
    n = N
    for gram in n_grams.keys():
        grams.append(gram)
        # print(gram)
        n -= 1
        if n == 0:
            break
    print(grams)
    for gram in grams:
        print(get_gram_sentence(gram, content))




# html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
# bsObj = BeautifulSoup(html, "html.parser")
# content = bsObj.find("div", {"id": "mw-content-text"}).get_text()
content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(),'utf-8')
theme = []   # 存储文本的主题句
# n_grams = n_grams("i am wayne, what is your name ?", 2)
n_grams = get_ngrams(content, 2)
# print(content)
n_grams = OrderedDict(sorted(n_grams.items(), key=lambda t: t[1], reverse=True))
# n_grams = OrderedDict(sorted(n_grams.items(), key=operator.itemgetter(1), reverse=True))
# lambda t:t[1] 等于operator.itemgetter(1)
print(n_grams)
print("2_grams count is:"+str(len(n_grams)))

# print(get_gram_sentence("united states", content))
get_theme(n_grams, 5, content)