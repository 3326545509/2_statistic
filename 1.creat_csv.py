#----- purpose ------
# statistic data of all SACs and creadte a csv
#--------------------

import csv
import os
from obspy import read

pathdata='/home/y_piao/work/2_test/4-6'
houzuis=['33to25','25to20']

def process_a_houzui(houzui):
    sacs=[]
    for dirpath, dirnames, filenames in os.walk(pathdata):
        for temp in filenames:
            #print(temp)
            if temp.split('_sec')[1]==houzui:
                sacs.append(os.path.join(dirpath, temp))
    print('-----lensacs: ',len(sacs))

    with open(houzui+'.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        heads=['id','houzui','date','time','evlo','evla','stlo','stla','dist','depmax','mag','az','baz','sn']
        writer.writerow(heads)
        for sac in sacs:
            templist=[]
            tr=read(sac)[0]
            templist.append(tr.id)
            templist.append(houzui)

            date_time=str(tr.stats.starttime+tr.stats.sac.o)
            templist.append(date_time.split("T")[0])
            templist.append(date_time.split("T")[1].split('0000Z')[0])

            templist.append(tr.stats.sac.evlo)
            templist.append(tr.stats.sac.evla)
            templist.append(tr.stats.sac.stlo)
            templist.append(tr.stats.sac.stla)
            templist.append(tr.stats.sac.dist)
            templist.append(tr.stats.sac.depmax)
            templist.append(tr.stats.sac.mag)
            templist.append(tr.stats.sac.az)
            templist.append(tr.stats.sac.baz)
            templist.append(tr.stats.sac.user0)
            writer.writerow(templist)
    print('-----houzui:',houzui,' is ok')

os.system('mkdir csv')
for houzui in houzuis:
    process_a_houzui(houzui)
    os.system('mv '+houzui+'.csv'+' ./csv')
