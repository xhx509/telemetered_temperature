# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:01:31 2015

Based on vitali's program 'sh_chkTBath', plot a graph to compare minilog1 and 2, 
#check hard iron correction

@author: hxu
"""

# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import glob
#from drifter_functions import colors
import pandas as pd
from pandas import *
from dateutil.parser import parse

# run with LSaveCFG=0 to check if evrything is alright
# then enable saving by setting LSaveCFG=1
LSaveCFG=0 
#LSaveCFG=1

#Here is the bath data from 09 April 2015
#all times are UTC
TBath_DATE='2015-04-09'
DTBath=[
# T_degC, Time1_UTC, Time2_UTC
 0.1028,'13:53:00','14:04:00',
 5.0005,'14:42:00','14:53:00',
 9.9991,'15:35:00','15:46:00',
15.0049,'16:31:00','16:42:00',
20.0014,'17:19:00','17:29:00',
]
TBath_Te=np.array(DTBath[0::3])
TBath_T1=DTBath[1::3]
TBath_T2=DTBath[2::3]
TBath_t1 = np.array([datetime.strptime(TBath_DATE+TBath_T1[k],'%Y-%m-%d%H:%M:%S') for k in range(len(TBath_T1))])
TBath_t2 = np.array([datetime.strptime(TBath_DATE+TBath_T2[k],'%Y-%m-%d%H:%M:%S') for k in range(len(TBath_T2))])

FN=glob.glob('*.csv') # get all csv files in 1 folder
#rgbcolor=colors(len(FN))
CLR=['r','g','b','m','c','y']
CLR=CLR*8



for k in range(len(FN)):
#rgbcolor=colors(len(ids)) # set plot color
    variables=['date','tim','temp']
    skipr=8     #get rid of first 8 rows
    dt=read_csv(FN[k],sep=',',skiprows=skipr,parse_dates={'time':[0,1]},date_parser=parse,names=variables,nrows=150)  #read minilog data
    time_ori=dt['time'].tolist()
    
    import datetime
    t=np.array([(datetime.datetime.strptime(str(q),'%Y-%m-%d %H:%M:%S')+datetime.timedelta(hours=4)) for q in time_ori])  #time transition
    for b in t:
        if b-datetime.datetime(2015, 4, 10, 0, 1)>datetime.timedelta(0):
            print FN[k]   
   #datetime.datetime.fromtimestamp(). strptime('%Y-%m-%d %H:%M:%S')
    temp_ori=dt['temp'].tolist()
    #num=num+1
    label_s=FN[k].find('_')+1
    label_e=FN[k].find('_',label_s+1)
    
    Te=TBath_Te*0.
    for kk in range(len(TBath_Te)):    
        i=np.argwhere((t>=TBath_t1[kk])&(t<TBath_t2[kk])).flatten()
        Te[kk]=dt['temp'][i].mean()
                                    
        #plt.plot([TBath_t1[kk],TBath_t2[kk]],[Te[kk],Te[kk]],'k-')      
        #plt.plot([TBath_t1[kk],TBath_t2[kk]],[TBath_Te[kk],TBath_Te[kk]],'g-')      
    #plt.xlabel('time')
    #plt.ylabel('T, degC')
    #plt.title(FN)
    #plt.show()        
    
    fig=plt.figure(101);
    if label_e-label_s>=5:
        
        plt.plot(TBath_Te,Te-TBath_Te,CLR[k]+'o-',label=FN[k][label_s:label_e])
    else:
        plt.plot(TBath_Te,Te-TBath_Te,CLR[k]+'o--',label=FN[k][label_s:label_e])
    ax= fig.add_subplot(111)
    
    ax.text(0.5,0.1, 'Minilog 1 : --- \n Minilog 2:___',
            verticalalignment='bottom', horizontalalignment='center',
            transform=ax.transAxes,
            color='black', fontsize=16)    
    plt.legend()
    plt.xlabel('Bath T,decC')
    plt.ylabel('deltaT, degC')
    plt.title('Minilog Temp Calibration Summary')

    
plt.show()            

