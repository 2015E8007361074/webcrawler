# coding:utf-8

"""
import datetime

# help(datetime)
print(dir(datetime))
help(datetime.time)

max = datetime.timezone(datetime.timedelta(0, 86340))
min = datetime.timezone(datetime.timedelta(-1, 60))
utc = datetime.timezone.utc
print(min)
print(datetime.date(2016, 1, 1))
print(datetime.__doc__)
print(datetime.time().hour)
"""
import time

print(time.localtime(time.time()))
# t = 1451923200
t= 1451577600
print(time.localtime(t))