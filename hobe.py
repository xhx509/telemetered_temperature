# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:49:05 2015

@author: hxu
"""
from pandas import *
import xlrd
from dateutil.parser import parse
import matplotlib.pyplot as plt
import matplotlib.dates as md

path = "SN 10708774 2015-04-21 12:27:55 -0400.xlsx"
book = xlrd.open_workbook(path)
location=book.sheet_by_index(2).row_slice(rowx=11,
                                start_colx=3,
                                end_colx=4)
location=str(location[0])[5:]
lat1=int(location[2:4])
lat2=int(location[8:10])/60.0
lat3=int(location[11:13])/3600.0
lon1=-int(location[16:18])
lon2=-int(location[22:24])/60.0
lon3=-int(location[-5:-3])/3600.0
lat=round(lat1+lat2+lat3,4)
lon=round(lon1+lon2+lon3,4)
f='SN 10708774 2015-04-21 12:27:55 -0400.csv'
variables=['datetime','temp','1','2','3','4','5']
skipr=3   #get rid of first 8 rows
dt=read_csv(f,sep=',',date_parser=parse,skiprows=skipr,names=variables)  #read minilog data
dt=dt.drop(dt.index[[-1]])
time_ori=dt['datetime'].tolist()

import datetime
time_ori=[(datetime.datetime.strptime(str(q),'%Y-%m-%d %H:%M:%S')) for q in time_ori]  #time transition
#datetime.datetime.fromtimestamp(). strptime('%Y-%m-%d %H:%M:%S')
temp_ori=dt['temp'].tolist()

fig=plt.figure()   #set figure
ax=fig.add_subplot(111)
ax.plot(time_ori,temp_ori,label='HOBE',linewidth=3, color='r')

ax.set_ylabel('Temperature(F)',fontsize=18)  #plot
xfmt = md.DateFormatter('%Y-%m-%d %H:%M')   #set plot time axis format
ax.xaxis.set_major_formatter(xfmt)
ax.legend()
plt.gcf().autofmt_xdate() #beautify time axis
plt.title('On coordinate: '+str(lat)+' '+str(lon),fontsize=25)
#df1.plot(x='time',y='temp_cur')
plt.show()
plt.savefig('test'+'.png')  #save file