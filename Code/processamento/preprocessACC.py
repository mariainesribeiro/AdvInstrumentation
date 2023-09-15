# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:54:15 2021

@author: mines
"""
import numpy as np
import novainstrumentation as ni

def preprocessACC(ax, ay, az):
    #ax
    mean_ax=np.mean(ax)
    std_ax=np.std(ax)
    filtered_ax = ni.smooth(ax, window_len=10)
    normalized_ax = (filtered_ax - mean_ax ) / std_ax
    
    #ay
    mean_ay=np.mean(ay)
    std_ay=np.std(ay)
    filtered_ay = ni.smooth(ay, window_len=10)
    normalized_ay = (filtered_ay - mean_ay ) / std_ay
    
    #az
    mean_az=np.mean(az)
    std_az=np.std(az)
    filtered_az = ni.smooth(az, window_len=10)
    normalized_az = (filtered_az - mean_az ) / std_az
    
    return normalized_ax, normalized_ay, normalized_az