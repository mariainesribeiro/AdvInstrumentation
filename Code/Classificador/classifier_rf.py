# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 19:50:30 2021

@author: afo.rebelo
"""

import pandas as pd
from sklearn.model_selection import LeaveOneOut
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import novainstrumentation as ni
import tsfel as tfe
import csv



def preprocess(data):
    """Preprocesses raw data, by smoothing it and removing mean of each axis"
   
    Parameters
    ----------
    x: nd-array - size (201x3)
        Raw data
            - each column represents the time series of an axis (X, Y, Z)
    
    Returns
    -------
    pp_data: nd-array - size(201x3)
        Preprocessed data
    
    """
    #Smoothing
    data[:,0] = ni.smooth(data[:,0], window_len=10)
    data[:,1] = ni.smooth(data[:,1], window_len=10)
    data[:,2] = ni.smooth(data[:,2], window_len=10)
    #Removing mean 
    mean_data_x = np.mean(data[:,0])
    mean_data_y = np.mean(data[:,1])
    mean_data_z = np.mean(data[:,2])
    pp_data = np.zeros((201,3))
    pp_data[:,0] = (data[:,0] - mean_data_x)  
    pp_data[:,1] = (data[:,1] - mean_data_y)  
    pp_data[:,2] = (data[:,2] - mean_data_z)
   
    return pp_data



def featureExtraction(data, fs):
    """Extraxts features from preprocessed data
   
    Parameters
    ----------
    data: nd-array - size (201x3)
        Preprocessed data from accelerometer
            - each column represents the time series of an axis (X, Y, Z)
    
    Returns
    -------
    features: list 
        20 extracted features
    
    """
    
    ax = data[:,0]
    ay = data[:,1]
    az = data[:,2]
    print(az)
    features = list()
    
    #human energy X
    features.append(tfe.human_range_energy(ax, fs))
    
    #Standard deviation X
    features.append(tfe.calc_std(ax))
    
    #Absolute energy X
    features.append(tfe.abs_energy(ax))
    
    #Total energy X
    features.append(tfe.total_energy(ax, fs))
                    
    #Autocorrelation X
    features.append(tfe.autocorr(ax))

    #RMS X
    features.append(tfe.rms(ax))
                    
    #Area under the curve X
    features.append(tfe.auc(ax, fs))
    
    #Standard deviation Z
    features.append(tfe.calc_std(az))
    
    #Total energy Z
    features.append(tfe.total_energy(az,fs))
                    
    #Area under the curve Z
    features.append(tfe.auc(az, fs))
    
    #Autocorrelation Z
    features.append(tfe.autocorr(az))
   
    #RMS Z
    features.append(tfe.rms(az))
    
    #Power bandwidth
    features.append(tfe.power_bandwidth(ax, fs))
    
    #Maximum Z
    features.append(tfe.calc_max(az))
    
    #Zero crossing rate
    features.append(tfe.zero_cross(ax))
    
    #Amplitude Z 
    features.append(tfe.calc_max(az)-tfe.calc_min(az))
    
    #Median frequency z
    features.append(tfe.median_frequency(ax, fs))
    
    #Minimum Z
    features.append(tfe.calc_min(az))
    
    #Standard deviation Y
    features.append(tfe.calc_std(ay))
    
    #Absolute energy Y
    features.append(tfe.abs_energy(ay))
    
    return features
    
    


def RandomForestTrain():
    """Trains the random forest classifier and returns evaluation
    
    Parameters
    ----------
    x: nd-array
        Reduced data with the selected features for each example
    
    Returns
    -------
    rf: 
        Random Forest trained classifier
    cm: nd-array
        Confusion matrix
    cr: nd-array
        Classification report with accuracy, precision, recall and f1-score
    
    """
    
    "Reads input examples for classifier"
    dataset = pd.read_csv("orange_output_numeros.csv")
    h = dataset.head(n=0)
    "Divide data into attributes and label"
    x = dataset.iloc[:, 0:20].values
    y = dataset.iloc[:, 20].values
    "Starting classifier"
    loo = LeaveOneOut()
    y_true, y_pred = list(), list()
    for train_index, test_index in loo.split(x):
        "Spliting the data"
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        "Training the classifier"
        model = RandomForestClassifier(random_state=0)
        model.fit(x_train, y_train)
        "Evaluating the classifier"
        y_hat = model.predict(x_test)
        y_true.append(y_test[0])
        y_pred.append(y_hat[0])
        
    cm = confusion_matrix(y_true,y_pred)
    cr = classification_report(y_true,y_pred)
    
    return model, cm, cr
    
model, cm, cr = RandomForestTrain()   
print('Matriz de confusão: \n-------------------\n\n', cm, '\n')
print('Relatório de Classificação: \n----------------------\n', cr)

