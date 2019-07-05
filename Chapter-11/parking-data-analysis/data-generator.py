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

import signal 
import sys 
import random 
from kafka.client import KafkaClient 
from kafka.consumer import SimpleConsumer 
from kafka.producer import SimpleProducer 
 
#Connect to kafka 
client = KafkaClient('ip-172-31-39-49.ec2.internal:6667') 
producer = SimpleProducer(client) 
 
class sensorMessage(object): 
    def __init__(self,lotId,spotId,timeStamp,occupied): 
        self.lotId         =     lotId 
        self.spotId         =     spotId 
        self.timeStamp     =     timeStamp 
        self.occupied    =    occupied 
 
    def getKey(self): 
        return self.timeStamp 
 
class parkingLot(object):     
    def __init__(self,lotId): 
        self.emptySpots = range(1,101) 
        self.lotId  = lotId 
     
    def getLotId(self): 
        return self.lotId 
         
    def getEmptySpotId(self): 
        if(len(self.emptySpots) != 0): 
            return random.choice(self.emptySpots) 
        else: 
            return 0     
 
class timeStamp(object): 
    def __init__(self): 
        self.hours         = range(0,24,1) 
        self.minutes     = range(0,60,1) 
        self.offset     = [1,1,1,1,1,2,2,4,4,8,8,8,8,8,8,8,8,6] 
 
    def getTime(self): 
        hour_start     = random.choice(self.hours) 
        min_start     = random.choice(self.minutes) 
        min_end = min_start 
        hour_end = (hour_start + random.choice(self.offset)) % 24  
        return (str(hour_start) + ":" + str(min_start),str(hour_end) + ":" + str(min_end)) 
 
def startParkingSession(lotId,spotId,timestamp): 
    return sensorMessage(lotId,spotId,timestamp,True) 
 
def endParkingSession(lotId,spotId,timestamp): 
    return sensorMessage(lotId,spotId,timestamp,False) 
 
parkingMessages = [] 
 
lots = [parkingLot(1),parkingLot(2),parkingLot(3)] 
 
timeObj = timeStamp() 
 
for i in range(0,200000): 
    lot     = random.choice(lots) 
    lotId     = lot.getLotId() 
    spotId     = lot.getEmptySpotId() 
 
    if spotId == 0: 
        continue 
 
    startTime,endTime = timeObj.getTime()     
 
    parkingMessages.append(startParkingSession(lotId,spotId,startTime)) 
    parkingMessages.append(endParkingSession(lotId,spotId,endTime)) 
 
parkingMessages.sort(key = lambda msg:msg.getKey()) 
 
for msg in parkingMessages: 
    x =  str(msg.lotId), str(msg.spotId), str(msg.timeStamp), 
    str(msg.occupied) 
    producer.send_messages("smartparking",bytes(x))
