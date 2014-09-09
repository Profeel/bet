#encoding:utf-8
#!/usr/local/bin/python2.7
from __future__ import division
import re
import os
import MySQLdb as mdb

def myAdd(x,y):
    return x+y

def myMin(x,y):
    return x-y

def preZjq(cur,gmdate,scr,w,d,l,a):
    sql_wd = "select zjq,count(*) from results where win between %s and %s and dog between %s and %s group by zjq order by count(*)" % (myMin(w,a),myAdd(w,a),myMin(d,a),myAdd(d,a))
    sql_dl = "select zjq,count(*) from results where dog between %s and %s and los between %s and %s group by zjq order by count(*)" % (myMin(d,a),myAdd(d,a),myMin(l,a),myAdd(l,a))
    sql_wl = "select zjq,count(*) from results where win between %s and %s or los between %s and %s group by zjq order by count(*)" % (myMin(w,a),myAdd(w,a),myMin(l,a),myAdd(l,a))
    temp_wl=["===胜负==="+"\n"]
    os.system("mkdir -p /mnt/hgfs/rh_share/%s" % gmdate)
    fn = "/mnt/hgfs/rh_share/%s/%s-%s.txt" % (str(gmdate),str(scr),str(w))
    f = open(fn,'w+')
    
    #文件-->添加总进球的标题
    data_zjq = []
    data_zjq.append("\n\n\n\t\t\t======总进球预测======\t\t\n")
    data_zjq.append(("\t\t\t======场次：%s======\t\t\t\n") % str(scr))
    data_zjq.append(("\t胜赔：%s\t 平赔: %s\t 负赔: %s \t精度:%s \n") % (str(w),str(d),str(l),str(a)))
    data_zjq.append("==========================================================================\n")
    data_zjq.append("\n===胜平===\t\n")
    sum_wd=0
    #wd_alldata:前4个进球数以及比例
    wd_alldata=[]
    #将SQL的所有结果保存到文件中
    cur.execute(sql_wd)
    for item in cur.fetchall():
        temp_wd_str1=str(item[0])+"球,"
        data_zjq.append(temp_wd_str1)
        temp1_wd=str(item[1])
        sum_wd+=item[1]
        temp_wd_str2 = re.search("\d{1,3}",temp1_wd).group()
        data_zjq.append(temp_wd_str2+'\n')
    data_zjq.append("总共-------->"+str(sum_wd)+"场\n===预测TOP3\n")
    cur.execute(sql_wd)
    for d in cur.fetchall():
        wd_alldata.append(str(d[0]))
        tmp4=str(d[1])
        temp_srt3 = re.search("\d{1,3}",tmp4).group()
        wd_alldata.append(temp_srt3)
    l = len(wd_alldata)
    if l==2:
        temp_wd_alldata = wd_alldata[-2:]
        data_zjq.append(str((temp_wd_alldata[0])+"球: 共")+str(temp_wd_alldata[1])+"场  占比:"+str(format(int(temp_wd_alldata[1])/sum_wd,".2%"))+"\n\n")
    elif l==4:
        temp_wd_alldata = wd_alldata[-4:]
        data_zjq.append(str((temp_wd_alldata[0])+"球:")+str(temp_wd_alldata[1])+"场  占比:"+str(format(int(temp_wd_alldata[1])/sum_wd,".2%"))+"\n")
        data_zjq.append(str((temp_wd_alldata[2])+"球:")+str(temp_wd_alldata[3])+"场  占比:"+str(format(int(temp_wd_alldata[3])/sum_wd,".2%"))+"\n\n")
    elif l>=6:
        temp_wd_alldata = wd_alldata[-6:]
        data_zjq.append(str((temp_wd_alldata[0])+"球: 共")+str(temp_wd_alldata[1])+"场  占比:"+str(format(int(temp_wd_alldata[1])/sum_wd,".2%"))+"\n")
        data_zjq.append(str((temp_wd_alldata[2])+"球: 共")+str(temp_wd_alldata[3])+"场  占比:"+str(format(int(temp_wd_alldata[3])/sum_wd,".2%"))+"\n")
        data_zjq.append(str((temp_wd_alldata[4])+"球: 共")+str(temp_wd_alldata[5])+"场  占比:"+str(format(int(temp_wd_alldata[5])/sum_wd,".2%"))+"\n\n")
    
    
    #平负
    sum_dl=0
    #dl_alldata:前4个进球数以及比例
    dl_alldata=[]
    data_zjq.append("\n===平负===\t\n")
    #将SQL的所有结果保存到文件中
    cur.execute(sql_dl)
    for item in cur.fetchall():
        temp_dl_str1=str(item[0])+"球,"
        data_zjq.append(temp_dl_str1)
        temp1_dl=str(item[1])
        sum_dl+=item[1]
        temp_dl_str2 = re.search("\d{1,3}",temp1_dl).group()
        data_zjq.append(temp_dl_str2+'\n')
    data_zjq.append("总共-------->"+str(sum_dl)+"场\n===预测TOP3\n")
    cur.execute(sql_dl)
    for d in cur.fetchall():
        dl_alldata.append(str(d[0]))
        tmp4=str(d[1])
        temp_srt3 = re.search("\d{1,3}",tmp4).group()
        dl_alldata.append(temp_srt3)
    l = len(dl_alldata)
    if l==2:
        temp_dl_alldata = dl_alldata[-2:]
        data_zjq.append(str((temp_dl_alldata[0])+"球: 共")+str(temp_dl_alldata[1])+"场  占比:"+str(format(int(temp_dl_alldata[1])/sum_dl,".2%"))+"\n\n")
    elif l==4:
        temp_dl_alldata = dl_alldata[-4:]
        data_zjq.append(str((temp_dl_alldata[0])+"球: 共")+str(temp_dl_alldata[1])+"场  占比:"+str(format(int(temp_dl_alldata[1])/sum_dl,".2%"))+"\n")
        data_zjq.append(str((temp_dl_alldata[2])+"球: 共")+str(temp_dl_alldata[3])+"场  占比:"+str(format(int(temp_dl_alldata[3])/sum_dl,".2%"))+"\n\n")
    elif l>=6:
        temp_dl_alldata = dl_alldata[-6:]
        data_zjq.append(str((temp_dl_alldata[0])+"球: 共")+str(temp_dl_alldata[1])+"场  占比:"+str(format(int(temp_dl_alldata[1])/sum_dl,".2%"))+"\n")
        data_zjq.append(str((temp_dl_alldata[2])+"球: 共")+str(temp_dl_alldata[3])+"场  占比:"+str(format(int(temp_dl_alldata[3])/sum_dl,".2%"))+"\n")
        data_zjq.append(str((temp_dl_alldata[4])+"球: 共")+str(temp_dl_alldata[5])+"场  占比:"+str(format(int(temp_dl_alldata[5])/sum_dl,".2%"))+"\n\n")
    
    #胜负
    sum_wl=0
    #wl_alldata:前4个进球数以及比例
    wl_alldata=[]
    data_zjq.append("\n===胜负===\t\n")
    #将SQL的所有结果保存到文件中
    cur.execute(sql_wl)
    for item in cur.fetchall():
        temp_wl_str1=str(item[0])+"球,"
        data_zjq.append(temp_wl_str1)
        temp1_wl=str(item[1])
        sum_wl+=item[1]
        temp_wl_str2 = re.search("\d{1,3}",temp1_wl).group()
        data_zjq.append(temp_wl_str2+'\n')
    data_zjq.append("总共-------->"+str(sum_wl)+"场\n===预测TOP3\n")
    cur.execute(sql_wl)
    for d in cur.fetchall():
        wl_alldata.append(str(d[0]))
        tmp4=str(d[1])
        temp_srt3 = re.search("\d{1,3}",tmp4).group()
        wl_alldata.append(temp_srt3)
    for item in temp_wl:
        f.writelines(str(item))
    l = len(wl_alldata)
    if l==2:
        temp_wl_alldata = wl_alldata[-2:]
        data_zjq.append(str((temp_wl_alldata[0])+"球: 共")+str(temp_wl_alldata[1])+"场  占比:"+str(format(int(temp_wl_alldata[1])/sum_wl,".2%"))+"\n\n")
    elif l==4:
        temp_wl_alldata = wl_alldata[-4:]
        data_zjq.append(str((temp_wl_alldata[0])+"球: 共")+str(temp_wl_alldata[1])+"场  占比:"+str(format(int(temp_wl_alldata[1])/sum_wl,".2%"))+"\n")
        data_zjq.append(str((temp_wl_alldata[2])+"球: 共")+str(temp_wl_alldata[3])+"场  占比:"+str(format(int(temp_wl_alldata[3])/sum_wl,".2%"))+"\n\n")
    elif l>=6:
        temp_wl_alldata = wl_alldata[-6:]
        data_zjq.append(str((temp_wl_alldata[0])+"球: 共")+str(temp_wl_alldata[1])+"场  占比:"+str(format(int(temp_wl_alldata[1])/sum_wl,".2%"))+"\n")
        data_zjq.append(str((temp_wl_alldata[2])+"球: 共")+str(temp_wl_alldata[3])+"场  占比:"+str(format(int(temp_wl_alldata[3])/sum_wl,".2%"))+"\n")
        data_zjq.append(str((temp_wl_alldata[4])+"球: 共")+str(temp_wl_alldata[5])+"场  占比:"+str(format(int(temp_wl_alldata[5])/sum_wl,".2%"))+"\n\n")
    data_zjq.append("============\n\n\n")
    for item in data_zjq:
        f.writelines(str(item)) 
    f.close()

def preSpf(cur,gmdate,scr,w,d,l,a):
    sql_spf_wd = "select spf,count(*) from results where win between %s and %s and dog between %s and %s group by spf order by count(*)" % (myMin(w,a),myAdd(w,a),myMin(d,a),myAdd(d,a))
    sql_spf_dl = "select spf,count(*) from results where dog between %s and %s and los between %s and %s group by spf order by count(*)" % (myMin(d,a),myAdd(d,a),myMin(l,a),myAdd(l,a))
    sql_spf_wl = "select spf,count(*) from results where win between %s and %s or los between %s and %s group by spf order by count(*)" % (myMin(w,a),myAdd(w,a),myMin(l,a),myAdd(l,a))

    data_spf = []
    data_spf.append("\n\n\n\t\t\t======胜平负预测======\t\t\n")
    data_spf.append(("\t\t\t======场次：%s======\t\t\t\n") % str(scr))
    data_spf.append(("\t胜赔：%s\t 平赔: %s\t 负赔: %s \t精度:%s \n") % (str(w),str(d),str(l),str(a)))
    data_spf.append("==========================================================================\n")
    data_spf.append("\n===胜平===\t\n")
    
    temp_spf_wd = []
    temp_spf_dl = []
    temp_spf_wl = []
    #写入到文件Precdiction.txt
    os.system("mkdir -p /mnt/hgfs/rh_share/%s" % gmdate)
    fn = "/mnt/hgfs/rh_share/%s/%s-%s.txt" % (str(gmdate),str(scr),str(w))
    f = open(fn,'a')
        
    #1.对于sql_spf_wd的输出进行处理
    cur.execute(sql_spf_wd)
    #统计胜平负场次总和
    sum_spf_wd=0
    #将SQL的所有结果保存到文件中
    for item in cur.fetchall():
        temp_spf_wd.append(str(item[0]))
        temp_spf_wd.append(str(item[1]))
        sum_spf_wd+=(item[1])
    #收集胜平负的场次，并求百分比
    #统计胜平负的比例
    cur.execute(sql_spf_wd)
    l = len(temp_spf_wd)
    data_spf.append(("场次: %s \n主赔+平陪-------->"+"一共 "+str(sum_spf_wd)+"场\n") % str(scr))
    if l==2:
        temp_spf_wd = temp_spf_wd[-2:]
        data_spf.append(str((temp_spf_wd[0])+":")+str(format(int(temp_spf_wd[1])/sum_spf_wd,".2%"))+"\n\n")
    elif l==4:
        temp_spf_wd = temp_spf_wd[-4:]
        data_spf.append(str((temp_spf_wd[0])+":")+str(format(int(temp_spf_wd[1])/sum_spf_wd,".2%"))+"\n")
        data_spf.append(str((temp_spf_wd[2])+":")+str(format(int(temp_spf_wd[3])/sum_spf_wd,".2%"))+"\n\n")
    elif l>=6:
        temp_spf_wd = temp_spf_wd[-6:]
        data_spf.append(str((temp_spf_wd[0])+":")+str(format(int(temp_spf_wd[1])/sum_spf_wd,".2%"))+"\n")
        data_spf.append(str((temp_spf_wd[2])+":")+str(format(int(temp_spf_wd[3])/sum_spf_wd,".2%"))+"\n")
        data_spf.append(str((temp_spf_wd[4])+":")+str(format(int(temp_spf_wd[5])/sum_spf_wd,".2%"))+"\n\n")
    
    #2.对于sql_spf_dl的输出进行处理
    cur.execute(sql_spf_dl)
    #统计胜平负场次总和
    sum_spf_dl=0
    data_spf.append("\n===胜平===\t\n")
    #将SQL的所有结果保存到文件中
    for item in cur.fetchall():
        temp_spf_dl.append(str(item[0]))
        temp_spf_dl.append(str(item[1]))
        sum_spf_dl+=(item[1])
    #统计胜平负的比例
    cur.execute(sql_spf_dl)
    l = len(temp_spf_dl)
    data_spf.append(("场次: %s \n平陪+负赔-------->"+"一共 "+str(sum_spf_dl)+"场\n") % str(scr))
    if l==2:
        temp_spf_dl = temp_spf_dl[-2:]
        data_spf.append(str((temp_spf_dl[0])+":")+str(format(int(temp_spf_dl[1])/sum_spf_dl,".2%"))+"\n\n")
    elif l==4:
        temp_spf_dl = temp_spf_dl[-4:]
        data_spf.append(str((temp_spf_dl[0])+":")+str(format(int(temp_spf_dl[1])/sum_spf_dl,".2%"))+"\n")
        data_spf.append(str((temp_spf_dl[2])+":")+str(format(int(temp_spf_dl[3])/sum_spf_dl,".2%"))+"\n\n")
    elif l>=6:
        temp_spf_dl = temp_spf_dl[-6:]
        data_spf.append(str((temp_spf_dl[0])+":")+str(format(int(temp_spf_dl[1])/sum_spf_dl,".2%"))+"\n")
        data_spf.append(str((temp_spf_dl[2])+":")+str(format(int(temp_spf_dl[3])/sum_spf_dl,".2%"))+"\n")
        data_spf.append(str((temp_spf_dl[4])+":")+str(format(int(temp_spf_dl[5])/sum_spf_dl,".2%"))+"\n\n")
        
    #3.对于sql_spf_wl的输出进行处理
    cur.execute(sql_spf_wl)
    #统计胜平负场次总和
    sum_spf_wl=0
    #将SQL的所有结果保存到文件中
    for item in cur.fetchall():
        temp_spf_wl.append(str(item[0]))
        temp_spf_wl.append(str(item[1]))
        sum_spf_wl+=(item[1])
    #统计胜平负的比例
    cur.execute(sql_spf_wl)
    l = len(temp_spf_wl)
    data_spf.append(("场次: %s \n胜赔+负赔-------->"+"一共 "+str(sum_spf_wl)+"场\n") % str(scr))
    if l==2:
        temp_spf_wl = temp_spf_wl[-2:]
        data_spf.append(str((temp_spf_wl[0])+":")+str(format(int(temp_spf_wl[1])/sum_spf_wl,".2%"))+"\n\n")
    elif l==4:
        temp_spf_wl = temp_spf_wl[-4:]
        data_spf.append(str((temp_spf_wl[0])+":")+str(format(int(temp_spf_wl[1])/sum_spf_wl,".2%"))+"\n")
        data_spf.append(str((temp_spf_wl[2])+":")+str(format(int(temp_spf_wl[3])/sum_spf_wl,".2%"))+"\n\n")
    elif l>=6:
        temp_spf_wl = temp_spf_wl[-6:]
        data_spf.append(str((temp_spf_wl[0])+":")+str(format(int(temp_spf_wl[1])/sum_spf_wl,".2%"))+"\n")
        data_spf.append(str((temp_spf_wl[2])+":")+str(format(int(temp_spf_wl[3])/sum_spf_wl,".2%"))+"\n")
        data_spf.append(str((temp_spf_wl[4])+":")+str(format(int(temp_spf_wl[5])/sum_spf_wl,".2%"))+"\n\n")
    data_spf.append("===============END OF 胜平负==================")
    for item in data_spf:
        f.writelines(item)
    f.close()
    
#=========================================
#比分预测    
def preRes(cur,gmdate,scr,w,d,l,a):
    sql_res_wd = "select res,count(*) from results where win between %s and %s and dog between %s and %s group by res order by count(*)" % (myMin(w,a),myAdd(w,a),myMin(d,a),myAdd(d,a))
    sql_res_dl = "select res,count(*) from results where dog between %s and %s and los between %s and %s group by res order by count(*)" % (myMin(d,a),myAdd(d,a),myMin(l,a),myAdd(l,a))
    sql_res_wl = "select res,count(*) from results where win between %s and %s or los between %s and %s group by res order by count(*)" % (myMin(w,a),myAdd(w,a),myMin(l,a),myAdd(l,a))
    
    data_res = []
    data_res.append("\n\n\n\t\t\t======比分预测======\t\t\n")
    data_res.append(("\t\t\t======场次：%s======\t\t\t\n") % str(scr))
    data_res.append(("\t胜赔：%s\t 平赔: %s\t 负赔: %s \t精度:%s \n") % (str(w),str(d),str(l),str(a)))
    data_res.append("==========================================================================\n")
    data_res.append("\n===胜平===\t\n")
    #统计比分的场次之和
    sum_res_wd = 0
    sum_res_dl = 0
    sum_res_wl = 0
    
    #暂存保存到文件的信息
    temp_res_wd = []
    temp_res_dl = []
    temp_res_wl = []
    
    #写入到文件
    os.system("mkdir -p /mnt/hgfs/rh_share/%s" % gmdate)
    fn = "/mnt/hgfs/rh_share/%s/%s-%s.txt" % (str(gmdate),str(scr),str(w))
    f = open(fn,'a')
        
    #1.对于sql_res_wd的输出进行处理
    cur.execute(sql_res_wd)
    #将SQL的所有结果保存到文件中
    for item in cur.fetchall():
        temp_res_wd.append(str(item[0]))
        temp_res_wd.append(str(item[1]))
        data_res.append(str(item[0])+": ")
        data_res.append("\t "+str(item[1])+" \n")
        sum_res_wd+=item[1]
    data_res.append("\n胜平预测------>\t"+str(sum_res_wd)+"场\n")
    #统计比分比例
    cur.execute(sql_res_wd)
    l = len(temp_res_wd)
    if l==4:
        temp_res_wd2 = temp_res_wd[-2:]
        data_res.append(str((temp_res_wd2[0])+"==》")+str(format(int(temp_res_wd2[1])/sum_res_wd,".2%"))+"\n")
    elif l==6:
        temp_res_wd2 = temp_res_wd[-4:]
        data_res.append(str((temp_res_wd2[0])+"==》")+str(format(int(temp_res_wd2[1])/sum_res_wd,".2%"))+"\n")
        data_res.append(str((temp_res_wd2[2])+"==》")+str(format(int(temp_res_wd2[3])/sum_res_wd,".2%"))+"\n\n")
    elif l>6:
        temp_res_wd2 = temp_res_wd[-8:]
        data_res.append(str((temp_res_wd2[0])+"==》")+str(format(int(temp_res_wd2[1])/sum_res_wd,".2%"))+"\n")
        data_res.append(str((temp_res_wd2[2])+"==》")+str(format(int(temp_res_wd2[3])/sum_res_wd,".2%"))+"\n")
        data_res.append(str((temp_res_wd2[4])+"==》")+str(format(int(temp_res_wd2[5])/sum_res_wd,".2%"))+"\n")
        data_res.append(str((temp_res_wd2[6])+"==》")+str(format(int(temp_res_wd2[7])/sum_res_wd,".2%"))+"\n\n")
    #2.对于sql_res_dl的输出进行处理
    cur.execute(sql_res_dl)
    cur.execute(sql_res_dl)
    #将SQL的所有结果保存到文件中
    for item in cur.fetchall():
        temp_res_dl.append(str(item[0]))
        temp_res_dl.append(str(item[1]))
        data_res.append(str(item[0])+": ")
        data_res.append("\t "+str(item[1])+" \n")
        sum_res_dl+=item[1]
    data_res.append("\n平负预测------>\t"+str(sum_res_dl)+"场\n")
    #统计比分比例
    cur.execute(sql_res_dl)
    l = len(temp_res_dl)
    if l==4:
        temp_res_dl2 = temp_res_dl[-2:]
        data_res.append(str((temp_res_dl2[0])+"==》")+str(format(int(temp_res_dl2[1])/sum_res_dl,".2%"))+"\n")
    elif l==6:
        temp_res_dl2 = temp_res_dl[-4:]
        data_res.append(str((temp_res_dl2[0])+"==》")+str(format(int(temp_res_dl2[1])/sum_res_dl,".2%"))+"\n")
        data_res.append(str((temp_res_dl2[2])+"==》")+str(format(int(temp_res_dl2[3])/sum_res_dl,".2%"))+"\n\n")
    elif l>6:
        temp_res_dl2 = temp_res_dl[-8:]
        data_res.append(str((temp_res_dl2[0])+"==》")+str(format(int(temp_res_dl2[1])/sum_res_dl,".2%"))+"\n")
        data_res.append(str((temp_res_dl2[2])+"==》")+str(format(int(temp_res_dl2[3])/sum_res_dl,".2%"))+"\n")
        data_res.append(str((temp_res_dl2[4])+"==》")+str(format(int(temp_res_dl2[5])/sum_res_dl,".2%"))+"\n")
        data_res.append(str((temp_res_dl2[6])+"==》")+str(format(int(temp_res_dl2[7])/sum_res_dl,".2%"))+"\n\n")
    
    #3.对于sql_res_wl的输出进行处理
    cur.execute(sql_res_wl)
    #将SQL的所有结果保存到文件中
    for item in cur.fetchall():
        temp_res_wl.append(str(item[0]))
        temp_res_wl.append(str(item[1]))
        data_res.append(str(item[0])+": ")
        data_res.append("\t"+str(item[1])+" \n")
        sum_res_wl+=item[1]
    data_res.append("\n胜负预测------>\t"+str(sum_res_wl)+"场\n")
    #统计比分比例
    cur.execute(sql_res_wl)
    l = len(temp_res_wl)
    if l==4:
        temp_res_wl2 = temp_res_wl[-2:]
        data_res.append(str((temp_res_wl2[0])+"==》")+str(format(int(temp_res_wl2[1])/sum_res_wl,".2%"))+"\n")
    elif l==6:
        temp_res_wl2 = temp_res_wl[-4:]
        data_res.append(str((temp_res_wl2[0])+"==》")+str(format(int(temp_res_wl2[1])/sum_res_wl,".2%"))+"\n")
        data_res.append(str((temp_res_wl2[2])+"==》")+str(format(int(temp_res_wl2[4])/sum_res_wl,".2%"))+"\n\n")
    elif l>6:
        temp_res_wl2 = temp_res_wl[-8:]
        data_res.append(str((temp_res_wl2[0])+"==》")+str(format(int(temp_res_wl2[1])/sum_res_wl,".2%"))+"\n")
        data_res.append(str((temp_res_wl2[2])+"==》")+str(format(int(temp_res_wl2[3])/sum_res_wl,".2%"))+"\n")
        data_res.append(str((temp_res_wl2[4])+"==》")+str(format(int(temp_res_wl2[5])/sum_res_wl,".2%"))+"\n")
        data_res.append(str((temp_res_wl2[6])+"==》")+str(format(int(temp_res_wl2[7])/sum_res_wl,".2%"))+"\n\n")
    data_res.append(("=============END OF THE Prediction of %s===================\n\n\n") % str(scr))
    #======END OF THE FUNCTION======
    for item in data_res:
        f.writelines(item)
    f.close()
    
def preAll(cur,gmdate,scr,w,d,l,a):
    preSpf(cur,gmdate,scr,w,d,l,a)
    preZjq(cur,gmdate,scr,w,d,l,a)
    preRes(cur,gmdate,scr,w,d,l,a)
    
if __name__=="__main__":
    conn=mdb.connect(host='localhost',user='root',passwd='oracle',db='betdb',port=3306)
    cur = conn.cursor()
    preAll(cur,"1000-09-06","001",1.55,3.60,5.00,0.01)