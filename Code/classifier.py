# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 19:50:30 2021

@author: afo.rebelo
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier #Regressor
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

dataset = pd.read_csv("orange_output.csv")
dataset.head()

"Divide data into attributes and label"
x = dataset.iloc[:, 0:15].values
y = dataset.iloc[:, 15].values

"Divide data into training and testing sets"
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

"Feature Scaling" #opcional (bom quando as escalas entre os valores são mt diferentes)
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

"Training the Algorithm"
regressor = RandomForestClassifier(n_estimators=200, random_state=0)
regressor.fit(x_train, y_train)
y_pred = regressor.predict(x_test)

"Evaluating the Algorithm"
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print(accuracy_score(y_test, y_pred))
