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
import preprocessACC as pp

myfile = open("output_lunges_others.csv", 'w')

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
"Lê ficheiros das Lungesões"
n=10
fs = 10 #TEMOS DE MUDAR ISTO
t_Lunges = np.zeros((n,201))
ax_Lunges = np.zeros((n,201))
ay_Lunges = np.zeros((n,201))
az_Lunges = np.zeros((n,201))

for e in range(n):
    "Read data file and extract time and accelerometer axis"
    filename = 'LungesAcc2_'+ str(e)
    file = 'C:\\Users\\Filipa Rebelo\\Desktop\\data_others\\LungesAcc1_'+ str(e) + '.csv'
    
    with open(file) as f:
        data = list(csv.reader(f, delimiter=','))

    data = np.array(data[1:], dtype=np.float)

    t_Lunges[e,:] = data[65:266,0]
    ax_Lunges[e,:] = data[65:266,1]
    ay_Lunges[e,:] = data[65:266,2]
    az_Lunges[e,:] = data[65:266,3]
    
    """*************************************************************************
    Preprocessamento"""
    ax_Lunges[e,:], ay_Lunges[e,:], az_Lunges[e,:] = pp.preprocessACC(ax_Lunges[e,:], ay_Lunges[e,:], az_Lunges[e,:])
    
    "*************************************************************************"

    "Time Domain Features"
    
    "Média do sinal para cada eixo"
    meanX= tfe.calc_mean(ax_Lunges[e,:])
    meanY= tfe.calc_mean(ay_Lunges[e,:])
    meanZ= tfe.calc_mean(az_Lunges[e,:])

    "Mediana do sinal para cada eixo"
    medianX= tfe.calc_median(ax_Lunges[e,:])
    medianY= tfe.calc_median(ay_Lunges[e,:])
    medianZ= tfe.calc_median(az_Lunges[e,:])
    
    "Desvio Padrão do sinal para cada eixo"
    stdX= tfe.calc_std(ax_Lunges[e,:])
    stdY= tfe.calc_std(ay_Lunges[e,:])
    stdZ= tfe.calc_std(az_Lunges[e,:])
   
    "Zero-crossing-rate do sinal para cada eixo"
    zcrX= tfe.zero_cross(ax_Lunges[e,:])
    zcrY= tfe.zero_cross(ay_Lunges[e,:])
    zcrZ= tfe.zero_cross(az_Lunges[e,:])  

    "Minimo do sinal para cada eixo"
    minX= tfe.calc_min(ax_Lunges[e,:])
    minY= tfe.calc_min(ay_Lunges[e,:])
    minZ= tfe.calc_min(az_Lunges[e,:])
    
    "Máximo do sinal para cada eixo" 
    maxX= tfe.calc_max(ax_Lunges[e,:])
    maxY= tfe.calc_max(ay_Lunges[e,:])
    maxZ= tfe.calc_max(az_Lunges[e,:])
    
    "Amplitude do sinal para cada eixo"
    ampX= minX-maxX
    ampY= minY-maxY
    ampZ= minZ-maxZ
    
    
    "Energia do sinal para cada eixo" #novo
    energiaX= tfe.abs_energy(ax_Lunges[e,:])
    energiaY= tfe.abs_energy(ay_Lunges[e,:])
    energiaZ= tfe.abs_energy(az_Lunges[e,:])
    
    "Energia total do sinal para cada eixo" #novo
    energiaTotalX= tfe.total_energy(ax_Lunges[e,:], fs)
    energiaTotalY= tfe.total_energy(ay_Lunges[e,:], fs)
    energiaTotalZ= tfe.total_energy(az_Lunges[e,:], fs)
    
    "Area under the curve" #novo
    aucX= tfe.auc(ax_Lunges[e,:], fs)
    aucY= tfe.auc(ay_Lunges[e,:], fs)
    aucZ= tfe.auc(az_Lunges[e,:], fs)
    
    "Autocorrelação" #novo
    autocorrX= tfe.autocorr(ax_Lunges[e,:])
    autocorrY= tfe.autocorr(ay_Lunges[e,:])
    autocorrZ= tfe.autocorr(az_Lunges[e,:])
    
    "Centroid" #Novo
    centroidX= tfe.calc_centroid(ax_Lunges[e,:], fs)
    centroidY= tfe.calc_centroid(ay_Lunges[e,:], fs)
    centroidZ= tfe.calc_centroid(az_Lunges[e,:], fs)
    
    "Root mean square" #Novo
    rmsX= tfe.rms(ax_Lunges[e,:])
    rmsY= tfe.rms(ay_Lunges[e,:])
    rmsZ= tfe.rms(az_Lunges[e,:])
    
    "*****************************************************************************"
    "Spectral Domain Features"
    
    "Human range energy"
    hrEnergyX = tfe.human_range_energy(ax_Lunges[e,:], fs)
    hrEnergyY = tfe.human_range_energy(ay_Lunges[e,:], fs)
    hrEnergyZ = tfe.human_range_energy(az_Lunges[e,:], fs)
    
    "Max power spectrum"
    maxPowerSpecX = tfe.max_power_spectrum(ax_Lunges[e,:], fs)
    maxPowerSpecY = tfe.max_power_spectrum(ay_Lunges[e,:], fs)
    maxPowerSpecZ = tfe.max_power_spectrum(az_Lunges[e,:], fs)
    
    "Maximum frequency"
    maxFreqX = tfe.max_frequency(ax_Lunges[e,:], fs)
    maxFreqY = tfe.max_frequency(ay_Lunges[e,:], fs)
    maxFreqZ = tfe.max_frequency(az_Lunges[e,:], fs)
    
    "Median frequency"
    medianFreqX = tfe.median_frequency(ax_Lunges[e,:], fs)
    medianFreqY = tfe.median_frequency(ay_Lunges[e,:], fs)
    medianFreqZ = tfe.median_frequency(az_Lunges[e,:], fs)
    
    "Power bandwidth"
    powerBandX = tfe.power_bandwidth(ax_Lunges[e,:], fs)
    powerBandY = tfe.power_bandwidth(ay_Lunges[e,:], fs)
    powerBandZ = tfe.power_bandwidth(az_Lunges[e,:], fs)
    
    "Spectral kurtosis"
    specKurtosisX = tfe.spectral_kurtosis(ax_Lunges[e,:], fs)
    specKurtosisY = tfe.spectral_kurtosis(ay_Lunges[e,:], fs)
    specKurtosisZ = tfe.spectral_kurtosis(az_Lunges[e,:], fs)
    
    "Spectral roll-off"
    specRollOffX = tfe.spectral_roll_off(ax_Lunges[e,:], fs)
    specRollOffY = tfe.spectral_roll_off(ay_Lunges[e,:], fs)
    specRollOffZ = tfe.spectral_roll_off(az_Lunges[e,:], fs)
    
    "Spectral skewness"
    specSkewnessX = tfe.spectral_skewness(ax_Lunges[e,:], fs)
    specSkewnessY = tfe.spectral_skewness(ay_Lunges[e,:], fs)
    specSkewnessZ = tfe.spectral_skewness(az_Lunges[e,:], fs)
    
    
    newrow = ('2' + ';' + str(meanX) + ';' + str(meanY) + ';' + str(meanZ) + ';' 
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
    
    