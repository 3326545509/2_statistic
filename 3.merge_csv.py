#-------
#比对csv文件和catlog，合并二者的信息
#-------
import os
import csv
from obspy.core import UTCDateTime
import numpy as np
from matplotlib import pyplot as plt

#---------------------
path='./csv/'
pathcatlog='./catlog.csv'
houzuis=['33to25','25to20']#,'20to17','17to15','15to13.2','13.2to11.7','11.7to10',\
#'10to8.5','8.5to7.3','7.3to6.4','6.4to5.5','5.5to4.8','4.8to4.25']
#---------------------

pathfs=[]
for houzui in houzuis:
    pathfs.append(path+houzui+'.csv')


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
    result=[]
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

    head=headf+headcatlog[5:]

    for i in range(1,len(dataf)):
        tempf=dataf[i]
        ft=tempf[ifdate]+'T'+tempf[iftime]
        ft=UTCDateTime(ft)
        fevlo=float(tempf[ifevlo])
        fevla=float(tempf[ifevla])

        for j in range(1,len(datacatlog)):
            tempcat=datacatlog[j]
            catt=tempcat[icatdata]+'T'+tempcat[icattime]
            catt=UTCDateTime(catt)
            catevlo=float(tempcat[icatevlo])
            catevla=float(tempcat[icatevla])
            #if abs(catt-ft)<20 and abs(catevlo-fevlo)<0.1 and abs(catevla-fevla)<0.1:
            errortmaxdist=0.4#rac not km
            errortmaxt=120
            #----将满足该条件的数据合并------------
            if abs(catt-ft-8*3600)<errortmaxt and abs(catevlo-fevlo)<errortmaxdist and abs(catevla-fevla)<errortmaxdist:
                #merge data
                #---create iresult, a list ; mag,stlo,stla,evlo,evla......
                iresult=tempf+tempcat[5:]
                result.append(iresult)
                break
    print('----- len result: ',len(result))
    print('----head',head)
    return result,head

def write(result,head,name):
    with open(name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(head)
        for iresult in result:
            writer.writerow(iresult)

os.system('mkdir mergeCSV')
for pathf in pathfs:
    f,catlog=read(pathf,pathcatlog)
    result,head=merge(f,catlog)
    name='3.merge.'+pathf.split('/')[2]
    write(result,head,name)
    os.system('mv '+name+' mergeCSV')