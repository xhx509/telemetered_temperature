# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:43:25 2015
simple plot for only plotting minilog
@author: hxu
"""
from dateutil.parser import parse
import numpy as np
import datetime
import pandas as pd
from pandas import *
import matplotlib.dates as md
import matplotlib.pyplot as plt
from drifter_functions import colors
import glob
f_ori_all=glob.glob('*.csv')
rgbcolor=colors(len(f_ori_all))
#f_ori='Minilog-II-T_353944_20150410_1.csv'
fig=plt.figure()   #set figure
ax=fig.add_subplot(111)
num=0

for f_ori in f_ori_all:
#rgbcolor=colors(len(ids)) # set plot color
    variables=['date','tim','temp']
    skipr=8     #get rid of first 8 rows
    dt=read_csv(f_ori,sep=',',skiprows=skipr,parse_dates={'time':[0,1]},date_parser=parse,names=variables,nrows=150)  #read minilog data
    time_ori=dt['time'].tolist()
    
    import datetime
    time_ori=[(datetime.datetime.strptime(str(q),'%Y-%m-%d %H:%M:%S')+datetime.timedelta(hours=4)) for q in time_ori]  #time transition
    for b in time_ori:
        if b-datetime.datetime(2015, 4, 10, 0, 1)>datetime.timedelta(0):
            print f_ori   
   #datetime.datetime.fromtimestamp(). strptime('%Y-%m-%d %H:%M:%S')
    temp_ori=dt['temp'].tolist()
    num=num+1
    label_s=f_ori.find('_')+1
    label_e=f_ori.find('_',label_s+1)
    

#f.writelines('site'+'         '+'lat         '+' lon        '+' depth(m)'+'    '+'      time'+'              '+'temp(C)'+'\n')
    ax.plot(time_ori,temp_ori,label=f_ori[label_s:label_e],linewidth=1, color=rgbcolor[num])
ax.set_ylabel('Temperature(C)',fontsize=18)  #plot
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')   #set plot time axis format
ax.xaxis.set_major_formatter(xfmt)
ax.legend()
plt.gcf().autofmt_xdate() #beautify time axis
#df1.plot(x='time',y='temp_cur')
plt.show()
plt.savefig('test1'+'.png')  #save file