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
myfile = open("output_flex_norm_amp.csv", 'w')
header = ('class;  medianX; medianY; medianZ;' +
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

n=22 #number of files 
fs = 10 #sampling rate
t_Flex = np.zeros((n,201))
ax_Flex = np.zeros((n,201))
ay_Flex = np.zeros((n,201))
az_Flex = np.zeros((n,201))

"****************************************************************************"
"                    READING AND PROCESSING EACH DATA FILE                   "
for e in range(n):
    "Read data file and extract time and accelerometer axis"
    file =  r'C:\Users\mines\Documents\Inês\FlexAcc2_'+ str(e) + '.csv'   
    with open(file) as f:
        data = list(csv.reader(f, delimiter=','))
    data = np.array(data[1:], dtype=np.float)
    #storing data and slicing the first samples, representing preparation time
    t_Flex[e,:] = data[65:266,0]
    ax_Flex[e,:] = data[65:266,1]
    ay_Flex[e,:] = data[65:266,2]
    az_Flex[e,:] = data[65:266,3]
    
    """**********************************************
    PREPROCESSING
        - smoothing with a sliding window of 10 samples
        - removing the mean of the signal
    """
    ax_Flex[e,:], ay_Flex[e,:], az_Flex[e,:] = pp.preprocessACC(ax_Flex[e,:], ay_Flex[e,:], az_Flex[e,:])
    
    """"*********************************************
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
    medianX= tfe.calc_median(ax_Flex[e,:])
    medianY= tfe.calc_median(ay_Flex[e,:])
    medianZ= tfe.calc_median(az_Flex[e,:])
    
    "Standard Deviation"
    stdX= tfe.calc_std(ax_Flex[e,:])
    stdY= tfe.calc_std(ay_Flex[e,:])
    stdZ= tfe.calc_std(az_Flex[e,:])
   
    "Zero-crossing-rate"
    zcrX= tfe.zero_cross(ax_Flex[e,:])
    zcrY= tfe.zero_cross(ay_Flex[e,:])
    zcrZ= tfe.zero_cross(az_Flex[e,:])  

    "Minimum"
    minX= tfe.calc_min(ax_Flex[e,:])
    minY= tfe.calc_min(ay_Flex[e,:])
    minZ= tfe.calc_min(az_Flex[e,:])
    
    "Maximum" 
    maxX= tfe.calc_max(ax_Flex[e,:])
    maxY= tfe.calc_max(ay_Flex[e,:])
    maxZ= tfe.calc_max(az_Flex[e,:])
    
    "Amplitude"
    ampX= minX-maxX
    ampY= minY-maxY
    ampZ= minZ-maxZ
    
    "Absolute energy" 
    energiaX= tfe.abs_energy(ax_Flex[e,:])
    energiaY= tfe.abs_energy(ay_Flex[e,:])
    energiaZ= tfe.abs_energy(az_Flex[e,:])
    
    "Total energy"
    energiaTotalX= tfe.total_energy(ax_Flex[e,:], fs)
    energiaTotalY= tfe.total_energy(ay_Flex[e,:], fs)
    energiaTotalZ= tfe.total_energy(az_Flex[e,:], fs)
    
    "Area under the curve" 
    aucX= tfe.auc(ax_Flex[e,:], fs)
    aucY= tfe.auc(ay_Flex[e,:], fs)
    aucZ= tfe.auc(az_Flex[e,:], fs)
    
    "Autocorrelation" 
    autocorrX= tfe.autocorr(ax_Flex[e,:])
    autocorrY= tfe.autocorr(ay_Flex[e,:])
    autocorrZ= tfe.autocorr(az_Flex[e,:])
    
    "Centroid" 
    centroidX= tfe.calc_centroid(ax_Flex[e,:], fs)
    centroidY= tfe.calc_centroid(ay_Flex[e,:], fs)
    centroidZ= tfe.calc_centroid(az_Flex[e,:], fs)
    
    "Root mean square" 
    rmsX= tfe.rms(ax_Flex[e,:])
    rmsY= tfe.rms(ay_Flex[e,:])
    rmsZ= tfe.rms(az_Flex[e,:])
    
    "Human range energy"
    hrEnergyX = tfe.human_range_energy(ax_Flex[e,:], fs)
    hrEnergyY = tfe.human_range_energy(ay_Flex[e,:], fs)
    hrEnergyZ = tfe.human_range_energy(az_Flex[e,:], fs)
    
    "Max power spectrum"
    maxPowerSpecX = tfe.max_power_spectrum(ax_Flex[e,:], fs)
    maxPowerSpecY = tfe.max_power_spectrum(ay_Flex[e,:], fs)
    maxPowerSpecZ = tfe.max_power_spectrum(az_Flex[e,:], fs)
    
    "Maximum frequency"
    maxFreqX = tfe.max_frequency(ax_Flex[e,:], fs)
    maxFreqY = tfe.max_frequency(ay_Flex[e,:], fs)
    maxFreqZ = tfe.max_frequency(az_Flex[e,:], fs)
    
    "Median frequency"
    medianFreqX = tfe.median_frequency(ax_Flex[e,:], fs)
    medianFreqY = tfe.median_frequency(ay_Flex[e,:], fs)
    medianFreqZ = tfe.median_frequency(az_Flex[e,:], fs)
    
    "Power bandwidth"
    powerBandX = tfe.power_bandwidth(ax_Flex[e,:], fs)
    powerBandY = tfe.power_bandwidth(ay_Flex[e,:], fs)
    powerBandZ = tfe.power_bandwidth(az_Flex[e,:], fs)
    
    "Spectral kurtosis"
    specKurtosisX = tfe.spectral_kurtosis(ax_Flex[e,:], fs)
    specKurtosisY = tfe.spectral_kurtosis(ay_Flex[e,:], fs)
    specKurtosisZ = tfe.spectral_kurtosis(az_Flex[e,:], fs)
    
    "Spectral roll-off"
    specRollOffX = tfe.spectral_roll_off(ax_Flex[e,:], fs)
    specRollOffY = tfe.spectral_roll_off(ay_Flex[e,:], fs)
    specRollOffZ = tfe.spectral_roll_off(az_Flex[e,:], fs)
    
    "Spectral skewness"
    specSkewnessX = tfe.spectral_skewness(ax_Flex[e,:], fs)
    specSkewnessY = tfe.spectral_skewness(ay_Flex[e,:], fs)
    specSkewnessZ = tfe.spectral_skewness(az_Flex[e,:], fs)
    
    """"*********************************************
    PRINTING COMPUTED FEATURES INTO CSV FILE
    """
    newrow = ('1' + ';' 
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
    
    