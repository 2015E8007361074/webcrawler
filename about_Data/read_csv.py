# coding:utf-8
from urllib.request import urlopen
from io import StringIO
import csv

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')
data_file = StringIO(data)
# csv_reader = csv.reader(data_file) # 直接读成列表的形式
csv_reader = csv.DictReader(data_file)  # 读成字典的形式
for row in csv_reader:
    print(row)