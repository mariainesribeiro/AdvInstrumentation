import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import os
import time
import numpy as np
import classifierRandomForest as crf
from sensordroid import Client
import countReps 

rf, cm, cr = crf.classifier()

flag=0
data=[]
AccValueData=5
n_sets_done = 0
n_get_ready = 0
workout_done = 0
reps =0

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

########################################################
#Routines of the server
# This class will be called when you visit or make a GET request
# to http:RASPIP:8888/ and will return the example.html page inside
# the static folder.
class index(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")
# Create a websocket between the client and the server
class WSHandler(tornado.websocket.WebSocketHandler):
    # Method called when a new client connects to the websocket
    def open(self):
        print('New Connection From:'+self.request.remote_ip)
    
    # This method called when a new message from a client arrive
    def on_message(self, message):
        global AccValueData
        global data
        global AccX
        global AccY
        global AccZ
        global n_sets_done
        global n_get_ready
        global workout_done
        global reps

        js = tornado.escape.json_decode(message)
        nSamples = 201
        nWait = 110
	
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
            if n_get_ready < 110:
                if n_get_ready == 0:
                    self.write_message({'class': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ]})
                else:
                    self.write_message({'class': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ] })
                n_get_ready = n_get_ready + 1
            elif  np.shape(data)[0]==0:
                self.write_message({'class': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ]})
                data = AccValueData
            elif np.shape(data)[0] < nSamples and np.shape(data)[0] > 0:
                self.write_message({'class': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ] }) 
                data = np.vstack((data, AccValueData))
            elif np.shape(data)[0] == nSamples:
                num = rf.predict([crf.features(crf.preprocess(data), 10)])
                if num == 1:
                    reps = countReps.countFlexReps(crf.preprocess(data)[:,0], 10)
                elif num == 2:
                    reps = countReps.countLungesReps(crf.preprocess(data)[:,2], 10)
                elif num == 3:
                    reps = countReps.countSquatReps(crf.preprocess(data)[:,2], 10)
                else:
                   pass
                self.write_message({'class': class_string(num), 'n_reps': reps, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ] }) 
                data = np.vstack((data, AccValueData))
                n_sets_done = n_sets_done + 1
            elif np.shape(data)[0] > nSamples and np.shape(data)[0] < nSamples + nWait:
                self.write_message({'class': 0, 'timestamp': time.time(), 'data': [AccX, AccY, AccZ] })
                data = np.vstack((data, AccValueData))
            elif np.shape(data)[0] == nSamples + nWait:
                data = []
            else:
                pass
        else:
            if workout_done == 0:
                workout_done = 1
                
# We need to tell our webserver what is the path to the static folder
settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}

# Maps a web address to a class
application = tornado.web.Application(handlers=[
    (r'/', index),
    (r'/ws', WSHandler)
], **settings)

#Launch Sensordroid
start = time.time()
Client.devicesDiscovered = devicesDiscoveredEventHandler
Client.startDiscovery()

# Launch our http server on port 9999
# http:RASPIP:99990/

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(9999)
print('Server Started in port 9999. ^C to kill')
tornado.ioloop.IOLoop.instance().start()

#close ServerDroid
Client.closeAll()
