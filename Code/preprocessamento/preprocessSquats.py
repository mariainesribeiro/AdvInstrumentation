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
import preprocess as pp

"*****************************************************************************"
"Lê ficheiros das flexões"
n=11
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

"Preprocessamento"
normalized_ax_Squat, filtered_ax_Squat, normalized_ay_Squat, filtered_ay_Squat, normalized_az_Squat, filtered_az_Squat = pp.preprocess(ax_Squat, ay_Squat, az_Squat)

#ax
plt.figure(figsize=(20,10))
plt.plot(t_Squat, ax_Squat,t_Squat, normalized_ax_Squat, t_Squat, filtered_ax_Squat)
plt.legend(('x', 'x_normalized', 'x_normalized_filtered'))
plt.title('Squats x', fontsize=20)
plt.xlabel('Time', fontsize=20)
plt.ylabel('Accelerometer', fontsize=20) 

#ay
plt.figure(figsize=(20,10))
plt.plot(t_Squat, ay_Squat, t_Squat, normalized_ay_Squat, t_Squat, filtered_ay_Squat)
plt.legend(('y', 'y_normalized', 'y_normalized_filtered'))
plt.title('Squats y', fontsize=20)
plt.xlabel('Time', fontsize=20)
plt.ylabel('Accelerometer', fontsize=20) 

#az
plt.figure(figsize=(20,10))
plt.plot(t_Squat, az_Squat, t_Squat, normalized_az_Squat, t_Squat, filtered_az_Squat)
plt.legend(('z', 'z_normalized', 'z_normalized_filtered'))
plt.title('Squats z', fontsize=20)
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

   