# coding:utf-8

import csv

csv_file = open("files/test.csv", "a+")  # a+表示再之前的基础上，添加信息

try:
    writer = csv.writer(csv_file)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(1000):
        writer.writerow((i, i+2, i*2))
finally:
    csv_file.close()