#encoding:utf-8
'''
Created on 2014-9-5

@author: Administrator
'''
#encoding:utf-8
from bs4 import BeautifulSoup
import urllib2
import re

def getLiveBet():
    '''
    get the live bet odd
    '''
    url="http://caipiao.163.com/order/jczq-hunhe/#from=leftnav"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    
    #scr
    i = 1
    screening = []
    for item in soup.findAll("span",{"class":"co1"}):
        screening.append(item.i.string)
        i+=1
    #scr_stoped
    for item in soup.findAll("dd"):
        if len(item.attrs)==16:
            if item.attrs[u'isstop']=='1':
                temp_stoped = re.search("\d{3}", item.attrs[u'matchnumcn']).group()
                #remove scrs has been stopped
                screening.remove(temp_stoped)
    
    #date
    gmdate = []
    for item in soup.findAll("span",{"class":"co3 gameTime"}):
            item_date = re.search("\d{4}-\d{2}-\d{2}",str(item)).group()
            item_time = item.i.string
            gmdate.append(item_date)
            gmdate.append(item_time)
    
    #hos
    i = 1
    hostTeam = []
    for item in soup.findAll("em",{"class":"hostTeam"}):
        hostTeam.append(item.b.string)
        i+=1
        
    #gue
    i = 1
    guestTeam = []
    for item in soup.findAll("em",{"class":"guestTeam"}):
        guestTeam.append(item.b.string)
        i+=1
    
    #spfpl
    #收集目前在售的场次的胜平负赔率
    #temp_spfpl包括让球胜平负赔率
    temp_spfpl = []
    for item in soup.findAll("span",{"class":"co6_1 btnBox towLine "}):
        for item2 in item.findAll("em"):
            #如果item2.string即赔率为“不支持当前比赛”的时候
            if len(item2.string)==10:
                temp_spfpl.append("0")
                temp_spfpl.append("0")
                temp_spfpl.append("0")
            else:
                temp_spfpl.append(item2.string)
    len_spf = len(temp_spfpl)/6
    spfpl =[]
    for j_spfpl in range(len_spf):
        spfpl.append(temp_spfpl[6*j_spfpl])
        spfpl.append(temp_spfpl[6*j_spfpl+1])
        spfpl.append(temp_spfpl[6*j_spfpl+2])
    
    #data收集
    data  = []
    l = len(spfpl)/3
    for i in range(l):
        #日期
        data.append(gmdate[2*i])
        #时间
        data.append(gmdate[2*i+1])
        #场次
        data.append(screening[i])
        #主队
        data.append(hostTeam[i])
        #客队
        data.append(guestTeam[i])
        #胜利赔率
        data.append(spfpl[3*i])
        #平赔率
        data.append(spfpl[3*i+1])
        #负赔率
        data.append(spfpl[3*i+2])
    return data

    
