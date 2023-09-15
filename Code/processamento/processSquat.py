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
import preprocessACC as pp

myfile = open("output_squat_others.csv", 'w')

header = ('class; meanX; meanY; meanZ; medianX; medianY; medianZ;' +
        'stdX; stdY; stdZ; zcrX; zcrY; zcrZ; minX; minY; minZ;' +
        'maxX; maxY; maxZ; ampX; ampY; ampZ;' +
        'energiaX; energiaY; energiaZ; energiaTotalX; energiaTotalY; energiaTotalZ;' +
        'aucX; aucY; aucZ; autocorrX; autocorrY; autocorrZ;' +
        'centroidX; centroidY; centroidZ; rmsX; rmsY; rmsZ;' +
        'hrEnergyX; hrEnergyY; hrEnergyZ;' +
        'maxPowerSpecX; maxPowerSpecY; maxPowerSpecZ; maxFreqX; maxFreqY; maxFreqZ;' +
        'medianFreqX; medianFreqY; medianFreqZ; powerBandX; powerBandY; powerBandZ;' +
        'specKurtosisX; specKurtosisY; specKurtosisZ;' +
        'specRollOffX; specRollOffY; specRollOffZ;' +
        'specSkewnessX; specSkewnessY; specSkewnessZ')


myfile.write(str(header) + "\n")

"*****************************************************************************"
"Lê ficheiros das flexões"
n=10
fs = 10 #TEMOS DE MUDAR ISTO
t_Squat = np.zeros((n,201))
ax_Squat = np.zeros((n,201))
ay_Squat = np.zeros((n,201))
az_Squat = np.zeros((n,201))

for e in range(n):
    "Read data file and extract time and accelerometer axis"
    print(e)
    filename = 'squatAcc2_'+ str(e)
    file = 'C:\\Users\\Filipa Rebelo\\Desktop\\data_others\\squatAcc1_'+ str(e) + '.csv'
    
    with open(file) as f:
        data = list(csv.reader(f, delimiter=','))

    data = np.array(data[1:], dtype=np.float)

    t_Squat[e,:] = data[50:251,0]
    ax_Squat[e,:] = data[50:251,1]
    ay_Squat[e,:] = data[50:251,2]
    az_Squat[e,:] = data[50:251,3]


    """*************************************************************************
    Preprocessamento"""
    ax_Squat[e,:], ay_Squat[e,:], az_Squat[e,:] = pp.preprocessACC(ax_Squat[e,:], ay_Squat[e,:], az_Squat[e,:])
    
    "*************************************************************************"
    "Time Domain Features"
    
    "Média do sinal para cada eixo"
    meanX= tfe.calc_mean(ax_Squat[e,:])
    meanY= tfe.calc_mean(ay_Squat[e,:])
    meanZ= tfe.calc_mean(az_Squat[e,:])

    "Mediana do sinal para cada eixo"
    medianX= tfe.calc_median(ax_Squat[e,:])
    medianY= tfe.calc_median(ay_Squat[e,:])
    medianZ= tfe.calc_median(az_Squat[e,:])
    
    "Desvio Padrão do sinal para cada eixo"
    stdX= tfe.calc_std(ax_Squat[e,:])
    stdY= tfe.calc_std(ay_Squat[e,:])
    stdZ= tfe.calc_std(az_Squat[e,:])
   
    "Zero-crossing-rate do sinal para cada eixo"
    zcrX= tfe.zero_cross(ax_Squat[e,:])
    zcrY= tfe.zero_cross(ay_Squat[e,:])
    zcrZ= tfe.zero_cross(az_Squat[e,:])  

    "Minimo do sinal para cada eixo"
    minX= tfe.calc_min(ax_Squat[e,:])
    minY= tfe.calc_min(ay_Squat[e,:])
    minZ= tfe.calc_min(az_Squat[e,:])
    
    "Máximo do sinal para cada eixo" 
    maxX= tfe.calc_max(ax_Squat[e,:])
    maxY= tfe.calc_max(ay_Squat[e,:])
    maxZ= tfe.calc_max(az_Squat[e,:])
    
    "Amplitude do sinal para cada eixo"
    ampX= minX-maxX
    ampY= minY-maxY
    ampZ= minZ-maxZ
    
    "Energia do sinal para cada eixo" #novo
    energiaX= tfe.abs_energy(ax_Squat[e,:])
    energiaY= tfe.abs_energy(ay_Squat[e,:])
    energiaZ= tfe.abs_energy(az_Squat[e,:])
    
    "Energia total do sinal para cada eixo" #novo
    energiaTotalX= tfe.total_energy(ax_Squat[e,:], fs)
    energiaTotalY= tfe.total_energy(ay_Squat[e,:], fs)
    energiaTotalZ= tfe.total_energy(az_Squat[e,:], fs)
    
    "Area under the curve" #novo
    aucX= tfe.auc(ax_Squat[e,:], fs)
    aucY= tfe.auc(ay_Squat[e,:], fs)
    aucZ= tfe.auc(az_Squat[e,:], fs)
    
    "Autocorrelação" #novo
    autocorrX= tfe.autocorr(ax_Squat[e,:])
    autocorrY= tfe.autocorr(ay_Squat[e,:])
    autocorrZ= tfe.autocorr(az_Squat[e,:])
    
    "Centroid" #Novo
    centroidX= tfe.calc_centroid(ax_Squat[e,:], fs)
    centroidY= tfe.calc_centroid(ay_Squat[e,:], fs)
    centroidZ= tfe.calc_centroid(az_Squat[e,:], fs)
    
    "Root mean square" #Novo
    rmsX= tfe.rms(ax_Squat[e,:])
    rmsY= tfe.rms(ay_Squat[e,:])
    rmsZ= tfe.rms(az_Squat[e,:])
    
    "*****************************************************************************"
    "Spectral Domain Features"
    
    "Human range energy"
    hrEnergyX = tfe.human_range_energy(ax_Squat[e,:], fs)
    hrEnergyY = tfe.human_range_energy(ay_Squat[e,:], fs)
    hrEnergyZ = tfe.human_range_energy(az_Squat[e,:], fs)
    
    "Max power spectrum"
    maxPowerSpecX = tfe.max_power_spectrum(ax_Squat[e,:], fs)
    maxPowerSpecY = tfe.max_power_spectrum(ay_Squat[e,:], fs)
    maxPowerSpecZ = tfe.max_power_spectrum(az_Squat[e,:], fs)
    
    "Maximum frequency"
    maxFreqX = tfe.max_frequency(ax_Squat[e,:], fs)
    maxFreqY = tfe.max_frequency(ay_Squat[e,:], fs)
    maxFreqZ = tfe.max_frequency(az_Squat[e,:], fs)
    
    "Median frequency"
    medianFreqX = tfe.median_frequency(ax_Squat[e,:], fs)
    medianFreqY = tfe.median_frequency(ay_Squat[e,:], fs)
    medianFreqZ = tfe.median_frequency(az_Squat[e,:], fs)
    
    "Power bandwidth"
    powerBandX = tfe.power_bandwidth(ax_Squat[e,:], fs)
    powerBandY = tfe.power_bandwidth(ay_Squat[e,:], fs)
    powerBandZ = tfe.power_bandwidth(az_Squat[e,:], fs)
    
    "Spectral kurtosis"
    specKurtosisX = tfe.spectral_kurtosis(ax_Squat[e,:], fs)
    specKurtosisY = tfe.spectral_kurtosis(ay_Squat[e,:], fs)
    specKurtosisZ = tfe.spectral_kurtosis(az_Squat[e,:], fs)
    
    "Spectral roll-off"
    specRollOffX = tfe.spectral_roll_off(ax_Squat[e,:], fs)
    specRollOffY = tfe.spectral_roll_off(ay_Squat[e,:], fs)
    specRollOffZ = tfe.spectral_roll_off(az_Squat[e,:], fs)
    
    "Spectral skewness"
    specSkewnessX = tfe.spectral_skewness(ax_Squat[e,:], fs)
    specSkewnessY = tfe.spectral_skewness(ay_Squat[e,:], fs)
    specSkewnessZ = tfe.spectral_skewness(az_Squat[e,:], fs)
    
    
    newrow = ('3' + ';' + str(meanX) + ';' + str(meanY) + ';' + str(meanZ) + ';' 
              + str(medianX) + ';' + str(medianY) + ';' + str(medianZ) + ';'
              + str(stdX) + ';' + str(stdY) + ';' + str(stdZ) + ';'
              + str(zcrX) + ';' + str(zcrY) + ';' + str(zcrZ) + ';'
              + str(minX) + ';' + str(minY) + ';' + str(minZ) + ';'
              + str(maxX) + ';' + str(maxY) + ';' + str(maxZ) + ';'
              + str(ampX) + ';' + str(ampY) + ';' + str(ampZ) + ';'
              + str(energiaX) + ';' + str(energiaY) + ';' + str(energiaY) + ';'
              + str(energiaTotalX) + ';' + str(energiaTotalY) + ';' + str(energiaTotalZ) + ';'
              + str(aucX) + ';' + str(aucY) + ';' + str(aucZ) + ';'
              + str(autocorrX) + ';' + str(autocorrY) + ';' + str(autocorrZ) + ';'
              + str(centroidX) + ';' + str(centroidY) + ';' + str(centroidZ) + ';'
              + str(rmsX) + ';' + str(rmsY) + ';' + str(rmsZ) + ';'
              + str(hrEnergyX) + ';' + str(hrEnergyY) + ';' + str(hrEnergyZ) + ';'
              + str(maxPowerSpecX) + ';' + str(maxPowerSpecY) + ';' + str(maxPowerSpecZ) + ';'
              + str(maxFreqX) + ';' + str(maxFreqY) + ';' + str(maxFreqZ) + ';'
              + str(medianFreqX) + ';' + str(medianFreqY) + ';' + str(medianFreqZ) + ';'
              + str(powerBandX) + ';' + str(powerBandY) + ';' + str(powerBandZ) + ';'
              + str(specKurtosisX) + ';' + str(specKurtosisY) + ';' + str(specKurtosisZ) + ';'
              + str(specRollOffX) + ';' + str(specRollOffY) + ';' + str(specRollOffZ) + ';'
              + str(specSkewnessX) + ';' + str(specSkewnessY) + ';' + str(specSkewnessZ))
    
    myfile.write(str(newrow) + '\n')

myfile.close()
    
    