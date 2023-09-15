# -*- coding: utf-8 -*-
"""
***************************************************************************
@authors: afo.rebelo & mid.ribeiro

"""
import numpy as np
import novainstrumentation as ni

def preprocessACC(ax, ay, az):
    """Preprocesses the input signal from each axis by:
        -smoothing with a sliding window of 10 samples
        - removing the mean
    
    Parameter:
    ---------
    ax: nd-array (1x201)
        X axis accelerometer signal
    
    ay: nd-array (1x201)
        Y axis accelerometer signal
        
    az: nd-array (1x201)
        Z axis accelerometer signal
    
    Returns:
    -------
    
    pp_ax: nd-array (1x201)
        Preprocessed X axis signal
    
    pp_ay: nd-array (1x201)
        Preprocessed Y axis signal
    
    pp_az: nd-array (1x201)
        Preprocessed Z axis signal
        
        
    """
     #ax
    filtered_ax = ni.smooth(ax, window_len=10)
    mean_ax=np.mean(filtered_ax)
    pp_ax = (filtered_ax - mean_ax )
    
    #ay
    filtered_ay = ni.smooth(ay, window_len=10)
    mean_ay=np.mean(filtered_ay)
    pp_ay = (filtered_ay - mean_ay ) 
    
    #az
    filtered_az = ni.smooth(az, window_len=10)
    mean_az=np.mean(filtered_az)
    pp_az = (filtered_az - mean_az ) 
    
    return pp_ax, pp_ay, pp_az