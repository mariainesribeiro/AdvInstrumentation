# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 17:01:30 2021

@author: afo.rebelo
"""

import numpy as np
import csv
from pylab import *
from scipy.stats import entropy
import novainstrumentation as ni
import tsfel.feature_extraction.features as tfe
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import preprocess as pp


"*****************************************************************************"
"Lê ficheiros das Lunges"
n=2
fs = 10 

"Read data file and extract time and accelerometer axis"
file = r'C:\Users\mines\Documents\Inês\LungesAcc2_'+ str(n) + '.csv'
    
with open(file) as f:
    data = list(csv.reader(f, delimiter=','))

data = np.array(data[1:], dtype=np.float)

t_Lunges = data[65:266,0]
ax_Lunges = data[65:266,1]
ay_Lunges = data[65:266,2]
az_Lunges = data[65:266,3]

"Preprocessamento"
normalized_ax_Lunges, filtered_ax_Lunges, normalized_ay_Lunges, filtered_ay_Lunges, normalized_az_Lunges, filtered_az_Lunges = pp.preprocess(ax_Lunges, ay_Lunges, az_Lunges)
#ax_Lunges
plt.figure(figsize=(20,10))
plt.plot(t_Lunges, ax_Lunges,t_Lunges, normalized_ax_Lunges, t_Lunges, filtered_ax_Lunges)
plt.legend(('x', 'x_normalized', 'x_normalized_filtered'))
plt.title('Lunges x', fontsize=20)
plt.xlabel('Time', fontsize=20)
plt.ylabel('Accelerometer', fontsize=20) 

#ay_Lunges
plt.figure(figsize=(20,10))
plt.plot(t_Lunges, ay_Lunges, t_Lunges, normalized_ay_Lunges, t_Lunges, filtered_ay_Lunges)
plt.legend(('y', 'y_normalized', 'y_normalized_filtered'))
plt.title('Lunges y', fontsize=20)
plt.xlabel('Time', fontsize=20)
plt.ylabel('Accelerometer', fontsize=20) 

#az_Lunges
plt.figure(figsize=(20,10))
plt.plot(t_Lunges, az_Lunges, t_Lunges, normalized_az_Lunges, t_Lunges, filtered_az_Lunges)
plt.legend(('z', 'z_normalized', 'z_normalized_filtered'))
plt.title('Lunges z', fontsize=20)
plt.xlabel('Time', fontsize=20)
plt.ylabel('Accelerometer', fontsize=20) 


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
    
    #cálculo da frequência fundamental do sinal
    lunges_freq = tfe.fundamental_frequency(z_data, fs)
    #cálculo da distância mínima entre picos consecutivos de uma flexão, com uma margem 
    min_distance = fs/lunges_freq*0.8
    #procura dos picos no sinal
    peaks = find_peaks(z_data, distance=min_distance)
    n_lunges = len(peaks[0])
    return n_lunges


print(countLungesReps(az_Lunges, fs))