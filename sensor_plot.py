# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 09:52:58 2014

Compare minilog sensor and blue by plotting a pic

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
f_ori='Minilog-II-T_356008_20150410_1.csv'                     #define  data files
f_cur='2015-04-15 10:44:43.csv'
#cur_id=24576
#input_time=[dt.datetime(2014,12,15,15,0,0,0,pytz.UTC),dt.datetime(2014,12,16,10,0,0,0,pytz.UTC)]

df1=pd.read_csv(f_cur,parse_dates={'time':[1]},date_parser=parse,names=np.array(['driftid','tme','temp_cur']))  #read file to get data

ids=[df1['driftid'][0]]  #get all ids of bluefish
for i in range(len(df1['driftid'])-1):
    if df1['driftid'][i+1]<>df1['driftid'][i]:
        ids.append(df1['driftid'][i+1])
rgbcolor=colors(len(ids)) # set plot color
variables=['date','tim','temp']
skipr=50    #get rid of first 8 rows
dt=read_csv(f_ori,sep=',',skiprows=skipr,parse_dates={'time':[0,1]},date_parser=parse,names=variables,nrows=110)  #read minilog data
time_ori=dt['time'].tolist()
import datetime
time_ori=[(datetime.datetime.strptime(str(q),'%Y-%m-%d %H:%M:%S')+datetime.timedelta(hours=4)) for q in time_ori]  #time transition
#datetime.datetime.fromtimestamp(). strptime('%Y-%m-%d %H:%M:%S')
temp_ori=dt['temp'].tolist()

fig=plt.figure()   #set figure
ax=fig.add_subplot(111)
num=0
f = open('./emolt'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '.xls', 'w')  # create file and name it

#f.writelines('site'+'         '+'lat         '+' lon        '+' depth(m)'+'    '+'      time'+'              '+'temp(C)'+'\n')
ax.plot(time_ori,temp_ori,label='minilog',linewidth=3, color='r')
for m in range(len(ids)):
    dfm=df1[df1['driftid'] == ids[m]]
    for n in range(len(dfm)):  # get data of a time period
        if str(dfm['time'].iloc[n])[0:13]=='2015-04-09 07':
            idx=n          
            continue
    for x in range(len(dfm)):
        if str(dfm['time'].iloc[x])[0:13]=='2015-04-09 16':
            idx2=x          
            continue    
    df2=dfm.iloc[idx:idx2]

    b_te,m_te=[],[]
    for y in range(len(df2)):
        for z in range(len(time_ori)):
            if time_ori[z].strftime('%Y-%m-%d %H:%M')==str(df2['time'].iloc[y])[0:16]:
                
                b_te.append(df2['temp_cur'].iloc[y])
                m_te.append(temp_ori[z])
    mean_mis=np.mean(b_te)-np.mean(m_te) ## Calculate mean value
    RMS=np.sqrt(sum([(b_te[z]-m_te[z])**2 for z in range(len(b_te))])/y) #calculate RMS
    print  ids[m], mean_mis , RMS ,y    
    f.writelines(str(ids[m])+','+ str(mean_mis)+','+ str(round(RMS,2))+ ','+str(y)+'\n' )    #write it to a file  
    
    temp_cur=df2['temp_cur'].tolist()
    bad_index=[]
    for p in range(len(temp_cur)):
        if temp_cur[p]<=0:
            bad_index.append(p)
    bad_index.reverse()

    time_cur=df2['time'].tolist()
    time_cur=[(j+datetime.timedelta(hours=5)) for j in time_cur]
    for i in bad_index:
        del    time_cur[i], temp_cur[i]
   
    #df1.plot(x='time',y='temp_cur')
    ax.plot(time_cur,temp_cur,label=ids[m],linewidth=2, color=rgbcolor[m])
f.close()
ax.set_ylabel('Temperature(C)',fontsize=18)  #plot
xfmt = md.DateFormatter('%Y-%m-%d %H:%M')   #set plot time axis format
ax.xaxis.set_major_formatter(xfmt)
ax.legend()
plt.gcf().autofmt_xdate() #beautify time axis
plt.title('Visible Assets vs Minilog',fontsize=25)
#df1.plot(x='time',y='temp_cur')
plt.show()
plt.savefig('test'+'.png')  #save file
