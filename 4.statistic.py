from matplotlib import pyplot as plt
import os
import numpy as np
from obspy.core import UTCDateTime
import csv
from scipy import stats


outdire='./4.statistic/'
indire='./3.mergeCSV/'
houzuis=['33to25']#,'25to20']#,'20to17','17to15','15to13.2','13.2to11.7','11.7to10',\
#'10to8.5','8.5to7.3','7.3to6.4','6.4to5.5','5.5to4.8','4.8to4.25']

def read(file):
    dataf=[]
    datacatlog=[]
    with open(file) as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            dataf.append(row)
    return dataf

def statistic(dataf):
    
    headf=dataf[0]
    ifdate=headf.index('date')
    iftime=headf.index('time')
    imag=headf.index('mag')
    idist=headf.index('dist')
    idepmax=headf.index('depmax')

    t0=UTCDateTime(dataf[1][ifdate]+'T'+dataf[1][iftime])
    events=[]
    event=[]
    for i in range(1,len(dataf)):
        t=UTCDateTime(dataf[i][ifdate]+'T'+dataf[i][iftime])
        if abs(t-t0)<5:
            #----时间差5s的记作同一个事件
            event.append(dataf[i])
            continue
        if len(event)>=10:
            #-----一个事件被10个台站记录到方为有效，记录太少了不做统计展示
            print('-----len event:',len(event))
            events.append(event)
        event=[]
        event.append(dataf[i])
        t0=t
    print('-----number of event,record>6: ',len(events))
    
    k=0
    for temp in events:
        k=k+len(temp)
    print('-----number of all sac:',k)
    
    return events,idist,idepmax,imag

def draw(events,idist,idepmax,imag,outfile):
    fig=plt.figure(figsize=(60,100))
    sumslope=[]
    summag=[]
    i=1

    for event in events:
        mag=float(event[0][imag])
        dist=[]
        depmax=[]
        #-----统计一个事件被记录到的全部点，用红色点表示
        for sac in event:
            if float(sac[idist])<100:
                continue
            dist.append(float(sac[idist]))
            depmax.append(np.log(float(sac[idepmax])*np.sqrt(float(sac[idist])/6371)))
        print('-----len depmax:',len(depmax))
        slope, intercept, r, p, se = stats.linregress(dist,depmax)

        fig.add_subplot(10,6,i)
        plt.cla()
        plt.scatter(dist,depmax,s=60,color='red')
        #plt.scatter(dist,slope*np.array(dist)+intercept,s=60,color='red')
        
        y=[]
        x=[]
        error=depmax-(slope*np.array(dist)+intercept)
        #-----统计3 sigma以内的点，用黑色点表示
        sigma=np.sqrt(sum((error-np.mean(error))**2))/len(error)
        for k in range(len(dist)):
            if abs(error[k])<3*sigma:
                y.append(depmax[k])
                x.append(dist[k])
        print('-----len x:',len(x))
        if len(x)==0:
            print(event[0][0],event[0][2])
            i=i+1
            continue
        
        plt.scatter(x,y,s=60,color='black')
        slope, intercept, r, p, se = stats.linregress(x,y)
        
        plt.title('black/all='+str(len(x))+'/'+str(len(dist))+' k='+'{:e}'.format(slope)+' mag(from SAC)='+str(mag))
        if len(x)>=10:
            sumslope.append(slope)
            summag.append(mag)
            plt.plot(x,slope*np.array(x)+intercept,color='blue')
        else:
            plt.plot(x,slope*np.array(x)+intercept,color='black')
        i=i+1
    avergeslope=sum(sumslope)/len(sumslope)
    fig.add_subplot(10,6,60)
    plt.scatter(summag,sumslope)
    plt.title('averge k='+'{:e}'.format(avergeslope))
    plt.xlabel('mag(from sac)')
    plt.ylabel('k')
    plt.tight_layout()
    plt.savefig(outdire+'/4.statistic'+outfile+'.png')

os.system('mkdir 4.statistic')
for houzui in houzuis:
    file=indire+'3.merge.'+houzui+'.csv'
    data=read(file)
    events,idist,idepmax,imag=statistic(data)
    draw(events,idist,idepmax,imag,houzui)