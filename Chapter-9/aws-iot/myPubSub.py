'''
MIT License

Copyright (c) 2019 Arshdeep Bahga and Vijay Madisetti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import datetime
import random

host = 'abc123-ats.iot.us-east-1.amazonaws.com'
rootCAPath = 'root-CA.crt'
certificatePath = 'AirQualityMonitor.cert.pem'
privateKeyPath = 'AirQualityMonitor.private.key'
clientId = 'basicPubSub'
topic = 'sdk/test/Python'
useWebsocket = False

# Port defaults
if useWebsocket:  
    port = 443
if not useWebsocket: 
    port = 8883

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, 
                                          useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, 
                        privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
# Infinite offline Publish queueing
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  
# Draining: 2 Hz
myAWSIoTMQTTClient.configureDrainingFrequency(2)  
# 10 sec
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  
 # 5 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5) 

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0

def getData():
    messageJson={}
    station=random.randint(0,1)
    if station==0:
        messageJson['stationID']='ST102'
        messageJson['latitude']=33.717950
        messageJson['longitude']=-84.454540
    elif station==1:
        messageJson['stationID']='ST105'
        messageJson['latitude']=33.933337
        messageJson['longitude']=-84.357290
    
    now=datetime.datetime.utcnow()
    messageJson['timestamp']=int(time.time())
    messageJson['pm2_5']=random.randint(0,5004)/10.0
    messageJson['pm10']=random.randint(0,6040)/10.0
    messageJson['o3']=random.randint(0,604)/1000.0
    messageJson['no2']=random.randint(65,204)/100.0
    messageJson['so2']=random.randint(0,1004)/1000.0
    messageJson['co']=random.randint(0,504)/100.0
    return messageJson

while True:        
    message = getData()
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print('Published topic %s: %s\n' % (topic, messageJson))
    loopCount += 1
    time.sleep(1)