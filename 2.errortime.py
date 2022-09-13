#------------------------
#在配对sac文件和catlog时发现事件的发震经纬度能对上，但是发震时刻总是对不上。
#于是挑一个频道的csv文件，统计其和catlog在发震位置相同时，记录的发震时刻的差值
#结论是二者几乎差8h，怀疑为北京时间和UTC时间的缘故。
#作图，图1是真实的时间差，图二是把图一8h附近的放大了的结果
#------------------------

import os
import csv
from obspy.core import UTCDateTime
import numpy as np
from matplotlib import pyplot as plt

pathf='./csv/33to25.csv'
pathcatlog='./catlog.csv'

def read(f,catlog):
    dataf=[]
    datacatlog=[]
    with open(f) as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            dataf.append(row)

    with open(catlog) as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            datacatlog.append(row)
    print('----len data f and catlog:',len(dataf),len(datacatlog))
    return dataf,datacatlog

def merge(dataf,datacatlog):
    #--------记录对于相同震源位置，sac文件里发震时刻和catlog里的差值--------
    errort=[]
    #--------------------
    headf=dataf[0]
    ifdate=headf.index('date')
    iftime=headf.index('time')
    ifevlo=headf.index('evlo')
    ifevla=headf.index('evla')
    #ifmag =headf.index('imag')

    headcatlog=datacatlog[0]
    icatdata=headcatlog.index('日期')
    icattime=headcatlog.index('时间')
    icatevlo=headcatlog.index('经度')
    icatevla=headcatlog.index('纬度')
    #icatmag =headcatlog.index('震级大小')

    t0=UTCDateTime(dataf[1][ifdate]+'T'+dataf[1][iftime])

    for i in range(1,len(dataf)):
        tempf=dataf[i]
        ft=tempf[ifdate]+'T'+tempf[iftime]
        ft=UTCDateTime(ft)
        if abs(ft-t0)<1:
            #----直到找到下一个发震时刻（即下一个地震事件时）执行下文
            continue
        else:
            t0=ft
        fevlo=float(tempf[ifevlo])
        fevla=float(tempf[ifevla])
        #----遍历catlog文件，查询发震位置相同的记录
        for j in range(1,len(datacatlog)):
            tempcat=datacatlog[j]
            catt=tempcat[icatdata]+'T'+tempcat[icattime]
            catt=UTCDateTime(catt)
            catevlo=float(tempcat[icatevlo])
            catevla=float(tempcat[icatevla])
            errormaxdist=0.4#rac not km
            if abs(catt-ft)<24*3600 and abs(catevlo-fevlo)<errormaxdist and abs(catevla-fevla)<errormaxdist:
                #----认为满足上述条件的为同一个地震，比较二者的时刻记录区别
                errort.append(abs(catt-ft))
                print(i,' is ok')
                break
        if len(errort)==0:
            #----即没有在catlog里匹配到相同的地震事件
            print('====== this earthquake dont match =======')
            continue
        print(min(errort)-8*3600)

    #----画图，不同地震事件的eror time
    fig=plt.figure(figsize=(20,10))
    plt.suptitle('error of evlo&evla <'+str(errormaxdist))
    fig.add_subplot(1,2,1)
    plt.title('error time, number of scatter:'+str(len(errort)))
    plt.scatter(range(len(errort)),np.array(errort)/3600,s=5)
    plt.xlabel('index of event')
    plt.ylabel('error time/hour')
    plt.yticks(range(0,25),range(0,25))

    fig.add_subplot(1,2,2)
    errortmaxt=30#容许的sac文件和catlog记录时刻的最大差值
    count=0
    #-----画图，不同地震事件的error time，把8小时附近的那些点放大出来
    for temp in errort:
        if abs(temp-8*3600)<errortmaxt:
            count=count+1
    plt.title('error time near 8h, number:'+str(count))
    plt.scatter(range(len(errort)),np.array(errort)-8*3600,s=5)
    plt.ylim(-1*errortmaxt,errortmaxt)
    plt.xlabel('index of event')
    plt.ylabel('error time/second')

    print('====error is: ',(np.mean(np.array(errort)))/3600)
    plt.savefig('./2.errortime.png')

f,catlog=read(pathf,pathcatlog)
merge(f,catlog)