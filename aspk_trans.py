# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 15:33:51 2014
Simple function is to convert units from hex to Decimal
in directory 'telemetered_temperature' 
@author: hxu
"""

def trans_latlon(string):
    if string[2]=='0' and string[3]=='0':
        string=string[0:2]+string[4:]
        
    lat=0.000010728836*int('0x'+string[4:10],16)
    lon=-0.000021457672*(16777216-int('0x'+string[10:16],16))
    print lat,lon
    return lat,lon
lat,lon=trans_latlon('0xA13B1F37CDC8149283')
print lat,lon