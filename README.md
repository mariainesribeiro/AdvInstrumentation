# AdvInstrumentation
Real-time physical exercise classifier and repetition counter.

## Goal
Create a real-time classification mobile web system for three types of physical exercises - squats, push-ups and lunges - and count the repetitions of each one.

## Scope 
Signals are acquired by the accelerometer of an Android device, and sent to a Linux virtual machine, wirelessly, through the Sensor Droid app.
The creation of this system is based on Machine Learning techniques with supervised classification. In other words, the classification of the signal collected in real time is based on previously known characteristics that explicitly distinguish the three types of movement – ​​the classes. In this way, the proposed classifier intends to assign, to a 20-second exercise, one of the four established classes. The fourth class is the rejection class, consisting of movements that do not fit into the three exercises mentioned above.

Firstly, the aim is to create, in offline mode, a dataset with several collections for each class. After pre-processing the collected signal, the aim is to extract the characteristics and select the most significant ones for building a classifier. To do this, the Orange software is used, which provides the input data for training the classifier. Finally, the built application aims to use communication via websockets between the browser (client) and the server, responsible for acquiring and classifying data collected online.

## Contents
### Code
Contains the code developed
Employed languages: python, javascript, html, css
### DemoImages
Contains images of a demo.
