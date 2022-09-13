import csv
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import os
from scipy import stats

#file='./test.csv'

outdire='./5.health/'
indire='./3.mergeCSV/'
houzuis=['33to25','25to20']#,'20to17','17to15','15to13.2','13.2to11.7','11.7to10',\
#'10to8.5','8.5to7.3','7.3to6.4','6.4to5.5','5.5to4.8','4.8to4.25']


def read(file):
    dataf=[]
    datacatlog=[]
    with open(file) as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            dataf.append(row)
    #dataf=dataf[1:]
    return dataf

def statistic_stations(dataf):
    headf   =   dataf[0]
    idepmax =   headf.index('depmax')
    imag    =   headf.index('mag')
    idist   =   headf.index('dist')
    iid     =   headf.index('id')
    
    ids=[   dataf[1][iid]  ]
    station=[   dataf[1]    ]
    stations=[  station     ]
    for i in range(1,len(dataf)):
        data=dataf[i]
        id  =data[iid]

        if id in ids:
            istation=ids.index(id)
            stations[istation].append(data)
        else:
            ids.append(id)
            station=[   data    ]
            stations.append(station)

    print('----len stations:',len(stations))
    sum2=[]
    for s in stations:
        sum2.append(len(s))
    print('----len sac number in station:\n',sum2)
    print('----len all sacs:',sum(np.array(sum2)))
    #print(stations[0])
    print('----a example:\n',stations[0][0])
    return stations,imag,idepmax,idist,iid

def draw(stations,imag,idepmax,idist,iid,houzui):
    fig=plt.figure(figsize=(40,200))
    norm=matplotlib.colors.Normalize(vmin=3,vmax=6)
    plt.suptitle('for each station, dist-amp-mag; x=dist/km,y=log10(amp)')
    i=1

    #--------test----------
    rs=[]
    ksmin=[]
    ksmax=[]
    ks=[]
    ids=[]
    #----------------------

    for station in stations:
        amp=[]
        ampmin=[]
        ampmax=[]
        dist=[]
        mag=[]
        for sac in station:
            #ampmin.append(float(sac[idepmax])*np.sqrt(4/(float(sac[imag])+0.5)))
            #ampmax.append(float(sac[idepmax])*np.sqrt(4/(float(sac[imag])-0.5)))
            amp.append(float(sac[idepmax])*(4/float(sac[imag])))
            dist.append(float(sac[idist]))
            mag.append(float(sac[imag]))
        fig.add_subplot(20,4,i)
        plt.cla()
        amp=np.array(amp)
        mag=np.array(mag)
        dist=np.array(dist)

        #x=np.log(1/np.sqrt(np.sin(dist/6371)))
        #y=np.log(np.array(amp))
        y=np.log10(amp*np.sqrt(4/mag))
        x=dist
        plt.ylim([0,6])
        plt.xlim([0,800])
        #------画辅助线--------
        x_fuzhu=np.arange(50,800)
        y_fuzhu=np.log10(1e5/x_fuzhu)
        y_fuzhu2=np.log10(1e4/x_fuzhu)
        y_fuzhu3=np.log10(1e3/x_fuzhu)
        plt.plot(x_fuzhu,y_fuzhu,'--')
        plt.plot(x_fuzhu,y_fuzhu2,'--')
        plt.plot(x_fuzhu,y_fuzhu3,'--')
        #ymin=np.log(np.array(ampmin))
        #ymax=np.log(np.array(ampmax))
        slope, intercept, r, p, se = stats.linregress(x,y)
        #slopemin, interceptmin, rmin, pmin, semin = stats.linregress(x,ymin)
        #slopemax, interceptmax, rmax, pmax, semax = stats.linregress(x,ymax)
        plt.plot(x,slope*np.array(x)+intercept,color='red')
        #plt.plot(x,slopemin*np.array(x)+interceptmin,color='blue')
        #plt.plot(x,slopemax*np.array(x)+interceptmax,color='green')

        rs.append(r)
        #ksmin.append(slopemin)
        #ksmax.append(slopemax)
        ks.append(slope)

        ids.append(sac[iid])
        sca=plt.scatter(x,y,s=180)#,c=mag,cmap='seismic',norm=norm)
        #plt.plot([0,800],[4,4],'--')
        #plt.plot([0,800],[2,2])
        #plt.plot([0,800],[5,5],':')
        
        #plt.ylim([0,10])
        #plt.xlim([1,3])
        plt.title(sac[iid])

        i=i+1

    #plt.colorbar(sca)

    # fig.add_subplot(20,4,77)
    # plt.scatter(range(len(ks)),ksmin)
    # plt.plot([0,len(ks)],[1,1],'--')
    # for i in range(len(ks)):
    #     plt.text(i,ksmin[i],ids[i])

    # fig.add_subplot(20,4,78)
    # plt.scatter(range(len(ks)),ksmax)
    # plt.plot([0,len(ks)],[1,1],'--')
    # for i in range(len(ks)):
    #     plt.text(i,ksmax[i],ids[i])

    fig.add_subplot(20,4,79)
    plt.scatter(range(len(ks)),ks)
    plt.plot([0,len(ks)],[0,0],'--')
    for i in range(len(ks)):
        with open('5.cold'+houzui+'.txt','a')as f:
            if ks[i]>0:
                f.write(ids[i]+'\n')
        plt.text(i,ks[i],ids[i])

    fig.add_subplot(20,4,80)
    plt.scatter(range(len(rs)),rs)
    for i in range(len(rs)):
        plt.text(i,rs[i],ids[i])

def moveCold(coldfile,scadatafile,outfile):
    os.system('sh 5.exclude_cold.sh '+coldfile+' '+scadatafile+' '+outfile)

os.system('mkdir '+outdire)
for houzui in houzuis:
    file=indire+'3.merge.'+houzui+'.csv'
    dataf=read(file)
    stations,imag,idepmax,idist,iid=statistic_stations(dataf)
    draw(stations,imag,idepmax,idist,iid,houzui)
    plt.tight_layout()
    plt.savefig(outdire+'5.health'+houzui+'.png',bbox_inches='tight')
    moveCold('5.cold'+houzui+'.txt',file,outdire+'3.health'+houzui+'.csv')
os.system('mv 5.cold*txt 5.health')