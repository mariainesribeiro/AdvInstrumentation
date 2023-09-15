# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:54:15 2021

@author: mines
"""
import numpy as np
import novainstrumentation as ni

def preprocess(ax, ay, az):
    #ax
    mean_ax=np.mean(ax)
    std_ax=np.std(ax)
    normalized_ax = (ax - mean_ax ) / std_ax
    filtered_ax = ni.smooth(normalized_ax, window_len=10)
    #ay
    mean_ay=np.mean(ay)
    std_ay=np.std(ay)
    normalized_ay = (ay - mean_ay ) / std_ay
    filtered_ay = ni.smooth(normalized_ay, window_len=10)
    #az
    mean_az=np.mean(az)
    std_az=np.std(az)
    normalized_az = (az - mean_az ) / std_az
    filtered_az = ni.smooth(normalized_az, window_len=10)
    
    return normalized_ax, filtered_ax, normalized_ay, filtered_ay, normalized_az, filtered_az
