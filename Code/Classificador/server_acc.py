import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
# The imports above are the function/classes we will need
# to lunch our webserver.
import os
import time
import numpy as np
import classifierRandomForest as crf
from sensordroid import Client

rf, cm, cr = crf.classifier()

flag=0
data=[]
AccValueData=5
n_sets_done = 0
n_get_ready = 0
workout_done = 0

#####################################################
# routines of the Sensordroid
def devicesDiscoveredEventHandler(devices):
    print(devices)
    if len(devices) > 0:
        client = Client(devices[0])

        client.connectionUpdated = connectionUpdatedEventHandler
        client.sensorsReceived = sensorsReceivedEventHandler

        client.sensorsSampleRate = 100

        client.connect()
        

def connectionUpdatedEventHandler(sender, msg):
    if sender is not None:
        if sender.connected:
            print("SensorDroid Connected")
        else:
            print("SeNsorDroid Disonnected") 

def sensorsReceivedEventHandler(sender, dataCurrent):
    global AccValueData
    global data
    global AccX
    global AccY
    global AccZ
    md=dataCurrent.Acceleration.Values.AsDouble
    AccX=md[0]
    AccY=md[1]
    AccZ=md[2]
    AccValueData = md
    #print(AccValueData) #print accelarometer data 0




########################################################
#Routines of the server


# This class will be called when you visit or make a GET request
# to http:RASPIP:8888/ and will return the example.html page inside
# the static folder.
class index(tornado.web.RequestHandler):
    def get(self):
        self.render("static/prof.html")
# This class is responsible to create a websocket between the client
# and the server, allowing for a persistent connection between them 
# and the hability of sending data in a fast and reliable way.
# To check the connection flow consult lab 9 readme.md file.
class WSHandler(tornado.websocket.WebSocketHandler):
    # This method will be called when a new client connects to the websocket
    def open(self):
        print('New Connection From:'+self.request.remote_ip)
        #print(type(self.request))
        #print(self.request)
        #print(self.request.remote_ip)
    
    # This method will be called when a new message from a client arrive
    def on_message(self, message):
        global AccValueData
        global data
        global AccX
        global AccY
        global AccZ
        global n_sets_done
        global n_get_ready
        global workout_done
        # Messages in websockets are usually passed as a JSON message (In string form).
        # JSON is more a less a dictionary, where you can have multiple
        # of key:values pairs.
        # The following line parses these json messages to python dictionaries
        js = tornado.escape.json_decode(message)
        nSamples = 201
        nWait = 99
	
        def class_string(val):
            if val == 1:
                workout = 'Push Ups'
            elif val == 2: 
                workout = 'Lunges' 
            elif val == 3: 
                workout = 'Squats'
            else:
                workout = 'Others'
            return workout

        n_sets = int(js['n_sets'])
        
        # This 'type' is define in our html page. 
        if(js['type'] == 'sendData' and n_sets > n_sets_done):
            #print("bip") 
	    
            if n_get_ready < 100:
                if n_get_ready == 0:
                    self.write_message({'class': 0, 'getReady': 1, 'workoutDone': 0, 'workout': 0, 'rest': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ]})
                    print('get ready 0') 
                else:
                    self.write_message({'class': 0, 'getReady': 0, 'workoutDone': 0, 'workout': 0, 'rest': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ] })
                print('get ready')  
                n_get_ready = n_get_ready + 1
            elif  np.shape(data)[0]==0:
                self.write_message({'class': 0, 'getReady': 0, 'workoutDone': 0, 'workout': 1, 'rest': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ]})
                print('go')   
                data = AccValueData
            elif np.shape(data)[0] < nSamples and np.shape(data)[0] > 0:
                self.write_message({'class': 0, 'getReady': 0, 'workoutDone': 0, 'workout': 0, 'rest': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ] }) 
                print('on going')  
                data = np.vstack((data, AccValueData))
            elif np.shape(data)[0] == nSamples:
                num = rf.predict([crf.features(crf.preprocess(data), 10)])
                print(class_string(num))
                self.write_message({'class': class_string(num), 'getReady': 0, 'workoutDone': 0, 'workout': 1, 'rest': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ] }) 
                data = np.vstack((data, AccValueData))
                n_sets_done = n_sets_done + 1
            elif np.shape(data)[0] > nSamples and np.shape(data)[0] < nSamples + nWait:
                self.write_message({'class': 0, 'getReady': 0, 'workoutDone': 0, 'workout': 0, 'rest': 1, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ] })
                data = np.vstack((data, AccValueData))
                print("Waiting")
            elif np.shape(data)[0] == nSamples + nWait:
                data = []
            else:
                pass
        else:
            if workout_done == 0:
                print('Workout done')
                workout_done = 1
                

# We need to tell our webserver what is the path to the static folder, since the
# html page will need to access files from this folder.
settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}

# Our server needs to know what to do when you navigate to a web address. The next
# function maps a web address to a class. r'/' is connected to index while
# r'/ws' is connected to web socket handler. This is called routing.

application = tornado.web.Application(handlers=[
    (r'/', index),
    (r'/ws', WSHandler)
], **settings)


#Launch Sensordroid
start = time.time()
Client.devicesDiscovered = devicesDiscoveredEventHandler
Client.startDiscovery()

# This will launch our http server on port 9999. To access it
# you need to navigate to http:RASPIP:99990/ and you should see
# the HTML page.

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(9999)
print('Server Started in port 9999. ^C to kill')
tornado.ioloop.IOLoop.instance().start()

#close ServerDroid
Client.closeAll()
