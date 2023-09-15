# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 17:01:30 2021

@author: afo.rebelo
"""

import numpy as np
import csv
from pylab import *
from scipy.stats import entropy
from scipy.signal import find_peaks
import novainstrumentation as ni
import tsfel.feature_extraction.features as tfe
import matplotlib.pyplot as plt

"*****************************************************************************"
"Lê ficheiros das flexões"
n=11 #número do ficheiro
fs = 10 
t_Flex = np.zeros((n,201))
ax_Flex = np.zeros((n,201))
ay_Flex = np.zeros((n,201))
az_Flex = np.zeros((n,201))


"Read data file and extract time and accelerometer axis"

file = r'C:\Users\mines\Documents\Inês\FlexAcc2_'+ str(n) + '.csv'
    
with open(file) as f:
    data = list(csv.reader(f, delimiter=','))

data = np.array(data[1:], dtype=np.float)

t_Flex = data[65:266,0]
ax_Flex = data[65:266,1]
ay_Flex = data[65:266,2]
az_Flex = data[65:266,3]



"Plot all data on same axis"
plt.figure(figsize=(20,10))
plt.plot(t_Flex, ax_Flex, t_Flex, ay_Flex, t_Flex, az_Flex)
plt.title('Flexões', fontsize=20)
plt.xlabel('Time', fontsize=20)
plt.ylabel('Accelerometer', fontsize=20)   

"******************************************************************************"
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


print(countFlexReps(ax_Flex,fs))

