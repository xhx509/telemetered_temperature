# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 15:33:51 2014

@author: hxu
"""

def trans_latlon(string):
    lat=0.000010728836*int('0x'+string[4:10],16)
    lon=0.000021457672*(16777216-int('0x'+string[10:16],16))
    return lat,lon
