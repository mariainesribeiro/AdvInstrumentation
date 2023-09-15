# -*- coding: utf-8 -*-
"""***************************************************************************
@authors: afo.rebelo & mid.ribeiro
***************************************************************************"""
from scipy.signal import find_peaks
import tsfel.feature_extraction.features as tfe


def countFlexReps(x_data, fs):
    """Counts the number of push ups done in 20 seconds
    
    Parameters
    ----------
    x_data: nd-array
        X axis accelerometer preprocessed signal 
    fs: int
        Sampling frequency
    
    Returns
    -------
    n_flex: 
        Number of push ups
    
    """
    
    #computes fundamental frequency 
    flex_freq = tfe.fundamental_frequency(x_data, fs)
    #computes minimum distance between consecutive peaks 
    min_distance = fs/flex_freq*0.8
    #finding peaks
    peaks = find_peaks(x_data, distance=min_distance)
    n_flex = len(peaks[0])
    return n_flex


def countLungesReps(z_data, fs):
    """Counts the number of lunges done in 20 seconds
    
    Parameters
    ----------
    z_data: nd-array
        Z axis accelerometer preprocessed signal 
    fs: int
        Sampling frequency
    
    Returns
    -------
    n_lunges: 
        Number of lunges
    
    """
    #signal inversion
    z_data = list(-z_data)
    #computes fundamental frequency
    lunges_freq = tfe.fundamental_frequency(z_data, fs)
    #computes minimum distance between consecutive peaks
    min_distance = fs/lunges_freq*0.8
    #finding peaks
    peaks = find_peaks(z_data, distance=min_distance)
    n_lunges = len(peaks[0])
    return n_lunges

def countSquatReps(z_data, fs):
    """Counts the number of squats done in 20 seconds
    
    Parameters
    ----------
    z_data: nd-array
        Z axis accelerometer preprocessed signal 
    fs: int
        Sampling frequency
    
    Returns
    -------
    n_squats: 
        Number of squats
    
    """
    z_data = list(-z_data)
    #computes fundamental frequency
    squats_freq = tfe.fundamental_frequency(z_data, fs)
    #computes minimum distance between consecutive peaks
    min_distance = fs/squats_freq*0.8
    #finding peaks
    peaks = find_peaks(z_data, distance=min_distance)
    n_squats = len(peaks[0])
    return n_squats

