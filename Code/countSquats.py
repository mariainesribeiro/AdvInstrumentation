# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 19:34:25 2020

@author: mines
"""

import numpy as np
import csv
from pylab import *
from scipy.stats import entropy
import novainstrumentation as ni
import tsfel.feature_extraction.features as tfe
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


"*****************************************************************************"
"Lê ficheiros das flexões"
n=14
fs = 10 
t_Squat = np.zeros((n,201))
ax_Squat = np.zeros((n,201))
ay_Squat = np.zeros((n,201))
az_Squat = np.zeros((n,201))


"Read data file and extract time and accelerometer axis"
file = r'C:\Users\mines\Documents\Inês\squatAcc2_'+ str(n) + '.csv'
    
with open(file) as f:
    data = list(csv.reader(f, delimiter=','))

data = np.array(data[1:], dtype=np.float)

t_Squat = data[65:266,0]
ax_Squat = data[65:266,1]
ay_Squat = data[65:266,2]
az_Squat = data[65:266,3]

"Plot all data on same axis"
plt.figure(figsize=(20,10))
plt.plot(t_Squat, az_Squat)#, t_Squat, ay_Squat, t_Squat, az_Squat)
plt.title('Squats', fontsize=20)
plt.xlabel('Time', fontsize=20)
plt.ylabel('Accelerometer', fontsize=20)   

"******************************************************************************"
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


print(countSquatReps(az_Squat,fs))

   