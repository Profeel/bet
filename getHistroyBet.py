#encoding:utf-8
'''
Created on 2014-9-9

@author: root
'''
from os import system
import datetime
def getHistoryBet(d):
    urls = []
    today = datetime.date.today()
    for i in range(d):
        yesterday = datetime.timedelta(days=i)
        urls.append("http://www.okooo.com/jingcai/bifen/jiangjin/"+str(today-yesterday))
    for item in urls:
        system("wget -U NoSuchBrowser/1.0 -P /root/bet/urls %s" % item)
    system("rm -f /root/bet/names.txt")
    system("ls /root/bet/urls > /root/bet/names.txt")
    system("python /root/bet/test.py")
