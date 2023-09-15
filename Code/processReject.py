# -*- coding: utf-8 -*-
"""***************************************************************************
@authors: afo.rebelo & mid.ribeiro

PROCESSING FLEX SEGMENTS 
    - reads the accelerometer data (axis X, Y, Z) from csv files, acquired offline
    - preprocesses the acc signals (smoothing and centering in zero, for each axis)
    - extracts features and saves them in a csv output file
    
***************************************************************************"""

import numpy as np
import csv
import tsfel.feature_extraction.features as tfe
import preprocessACC as pp

"Opening output file"
myfile = open("output_reject_norm_amp_other.csv", 'w')
header = ('class; medianX; medianY; medianZ;' +
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

n=10 #Number of files
fs = 10 #sampling frequency
t_Reject = np.zeros((n,201))
ax_Reject = np.zeros((n,201))
ay_Reject = np.zeros((n,201))
az_Reject = np.zeros((n,201))

"****************************************************************************"
"                    READING AND PROCESSING EACH DATA FILE                   "
for e in range(n):
    "Read data file and extract time and accelerometer axis"
    file = r'C:\Users\mines\Documents\Inês\other\RejectAcc1_'+ str(e) + '.csv'
    with open(file) as f:
        data = list(csv.reader(f, delimiter=','))
    data = np.array(data[1:], dtype=np.float)
    #storing data and slicing the first samples, representing preparation time
    t_Reject[e,:] = data[40:241,0]
    ax_Reject[e,:] = data[40:241,1]
    ay_Reject[e,:] = data[40:241,2]
    az_Reject[e,:] = data[40:241,3]


    """**********************************************
    PREPROCESSING
        - smoothing with a sliding window of 10 samples
        - removing the mean of the signal
    """
    ax_Reject[e,:], ay_Reject[e,:], az_Reject[e,:] = pp.preprocessACC(ax_Reject[e,:], ay_Reject[e,:], az_Reject[e,:])
    
    """""*********************************************
    FEATURE EXTRACTION
    
        - time domain features:
            -> zero crossing rate
            -> absolute energy
            -> total energy
            -> area under the curve
            -> autocorrelation
            -> centroid
        - statistical domain features:
            -> median
            -> standard deviation
            -> amplitude
            -> maximum
            -> minimum
            -> root mean square 
        - spectral domain features:
            -> human energy spectrum
            -> maximum power
            -> maximum frequency
            -> median frequency
            -> power spectrum bandwidth
            -> spectral kurtosis
            -> spectral skeweness
            -> rolloff
            
    """

    "Median"
    medianX= tfe.calc_median(ax_Reject[e,:])
    medianY= tfe.calc_median(ay_Reject[e,:])
    medianZ= tfe.calc_median(az_Reject[e,:])
    
    "Standard Deviation"
    stdX= tfe.calc_std(ax_Reject[e,:])
    stdY= tfe.calc_std(ay_Reject[e,:])
    stdZ= tfe.calc_std(az_Reject[e,:])
   
    "Zero-crossing-rate"
    zcrX= tfe.zero_cross(ax_Reject[e,:])
    zcrY= tfe.zero_cross(ay_Reject[e,:])
    zcrZ= tfe.zero_cross(az_Reject[e,:])  

    "Minimum"
    minX= tfe.calc_min(ax_Reject[e,:])
    minY= tfe.calc_min(ay_Reject[e,:])
    minZ= tfe.calc_min(az_Reject[e,:])
    
    "Maximum" 
    maxX= tfe.calc_max(ax_Reject[e,:])
    maxY= tfe.calc_max(ay_Reject[e,:])
    maxZ= tfe.calc_max(az_Reject[e,:])
    
    "Amplitude"
    ampX= minX-maxX
    ampY= minY-maxY
    ampZ= minZ-maxZ
    
    "Absolute energy"
    energiaX= tfe.abs_energy(ax_Reject[e,:])
    energiaY= tfe.abs_energy(ay_Reject[e,:])
    energiaZ= tfe.abs_energy(az_Reject[e,:])
    
    "Total energy"
    energiaTotalX= tfe.total_energy(ax_Reject[e,:], fs)
    energiaTotalY= tfe.total_energy(ay_Reject[e,:], fs)
    energiaTotalZ= tfe.total_energy(az_Reject[e,:], fs)
    
    "Area under the curve"
    aucX= tfe.auc(ax_Reject[e,:], fs)
    aucY= tfe.auc(ay_Reject[e,:], fs)
    aucZ= tfe.auc(az_Reject[e,:], fs)
    
    "Autocorrelation"
    autocorrX= tfe.autocorr(ax_Reject[e,:])
    autocorrY= tfe.autocorr(ay_Reject[e,:])
    autocorrZ= tfe.autocorr(az_Reject[e,:])
    
    "Centroid"
    centroidX= tfe.calc_centroid(ax_Reject[e,:], fs)
    centroidY= tfe.calc_centroid(ay_Reject[e,:], fs)
    centroidZ= tfe.calc_centroid(az_Reject[e,:], fs)
    
    "Root mean square" 
    rmsX= tfe.rms(ax_Reject[e,:])
    rmsY= tfe.rms(ay_Reject[e,:])
    rmsZ= tfe.rms(az_Reject[e,:])
    
    "Human range energy"
    hrEnergyX = tfe.human_range_energy(ax_Reject[e,:], fs)
    hrEnergyY = tfe.human_range_energy(ay_Reject[e,:], fs)
    hrEnergyZ = tfe.human_range_energy(az_Reject[e,:], fs)
    
    "Max power spectrum"
    maxPowerSpecX = tfe.max_power_spectrum(ax_Reject[e,:], fs)
    maxPowerSpecY = tfe.max_power_spectrum(ay_Reject[e,:], fs)
    maxPowerSpecZ = tfe.max_power_spectrum(az_Reject[e,:], fs)
    
    "Maximum frequency"
    maxFreqX = tfe.max_frequency(ax_Reject[e,:], fs)
    maxFreqY = tfe.max_frequency(ay_Reject[e,:], fs)
    maxFreqZ = tfe.max_frequency(az_Reject[e,:], fs)
    
    "Median frequency"
    medianFreqX = tfe.median_frequency(ax_Reject[e,:], fs)
    medianFreqY = tfe.median_frequency(ay_Reject[e,:], fs)
    medianFreqZ = tfe.median_frequency(az_Reject[e,:], fs)
    
    "Power bandwidth"
    powerBandX = tfe.power_bandwidth(ax_Reject[e,:], fs)
    powerBandY = tfe.power_bandwidth(ay_Reject[e,:], fs)
    powerBandZ = tfe.power_bandwidth(az_Reject[e,:], fs)
    
    "Spectral kurtosis"
    specKurtosisX = tfe.spectral_kurtosis(ax_Reject[e,:], fs)
    specKurtosisY = tfe.spectral_kurtosis(ay_Reject[e,:], fs)
    specKurtosisZ = tfe.spectral_kurtosis(az_Reject[e,:], fs)
    
    "Spectral roll-off"
    specRollOffX = tfe.spectral_roll_off(ax_Reject[e,:], fs)
    specRollOffY = tfe.spectral_roll_off(ay_Reject[e,:], fs)
    specRollOffZ = tfe.spectral_roll_off(az_Reject[e,:], fs)
    
    "Spectral skewness"
    specSkewnessX = tfe.spectral_skewness(ax_Reject[e,:], fs)
    specSkewnessY = tfe.spectral_skewness(ay_Reject[e,:], fs)
    specSkewnessZ = tfe.spectral_skewness(az_Reject[e,:], fs)
    
    """"*********************************************
    PRINTING COMPUTED FEATURES INTO CSV FILE
    """
    newrow = ('4' + ';' 
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
    
    