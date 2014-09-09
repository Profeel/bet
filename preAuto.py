'''
Created on 2014-9-5

@author: root
'''
from getLiveBet import getLiveBet
from pre import preAll
import MySQLdb as mdb

def preAuto():
    t = getLiveBet()
    l = len(t)/8
    conn=mdb.connect(host='localhost',user='root',passwd='oracle',db='betdb',port=3306)
    cur = conn.cursor()
    for i in range(l):
        if float(t[8*i+5])>0:
            preAll(cur,str(t[8*i]),str(t[8*i+2]),float(t[8*i+5]),float(t[8*i+6]),float(t[8*i+7]),0.05)

if __name__=="__main__":
    preAuto()
    print "Done!!!"