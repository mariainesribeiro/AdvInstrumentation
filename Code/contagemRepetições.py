# -*- coding: utf-8 -*-
import numpy as np
from scipy.signal import find_peaks
import tsfel.feature_extraction.features as tfe



def countFlexReps(x_data, fs):
    """Conta o número de flexões realizadas
    
    Parameters
    ----------
    x_data: nd-array
        Sinal do eixo x do acelerómeto 
    fs: int
        Frequência de amostragem
    
    Returns
    -------
    n_flex: 
        Número de flexões realizadas
    
    """
    
    #cálculo da frequência fundamental do sinal
    flex_freq = tfe.fundamental_frequency(x_data, fs)
    #cálculo da distância mínima entre picos consecutivos de uma flexão, com uma margem 
    min_distance = fs/flex_freq*0.8
    #procura dos picos no sinal
    peaks = find_peaks(x_data, distance=min_distance)
    #conta os picos
    n_flex = len(peaks[0])
    return n_flex


def countLungesReps(z_data, fs):
    """Conta o número de lunges realizadas
    
    Parameters
    ----------
    z_data: nd-array
        Sinal do eixo z do acelerómeto 
    
    Returns
    -------
    n_lunges: 
        Número de lunges realizadas
    
    """
    #inversão do sinal
    z_data = list(-z_data)
    plt.plot(t_Lunges, z_data)
    #cálculo da frequência fundamental do sinal
    lunges_freq = tfe.fundamental_frequency(z_data, fs)
    #cálculo da distância mínima entre picos consecutivos de uma flexão, com uma margem 
    min_distance = fs/lunges_freq*0.8
    #procura dos picos no sinal
    peaks = find_peaks(z_data, distance=min_distance)
    n_lunges = len(peaks[0])
    return n_lunges

def countSquatReps(z_data, fs):
    """Conta o número de squats realizadas
    
    Parameters
    ----------
    z_data: nd-array
        Sinal do eixo z do acelerómeto 
    
    Returns
    -------
    n_squat: 
        Número de squats realizados
    
    """
    z_data = list(-z_data)
    #cálculo da frequência fundamental do sinal
    squats_freq = tfe.fundamental_frequency(z_data, fs)

    #cálculo da distância mínima entre picos consecutivos de uma flexão, com uma margem 
    min_distance = fs/squats_freq*0.8
    #procura dos picos no sinal
    peaks = find_peaks(z_data, distance=min_distance)
    n_squats = len(peaks[0])
    return n_squats

def fatiasPizaQueimadas(n_series):
    return n_series*0.004