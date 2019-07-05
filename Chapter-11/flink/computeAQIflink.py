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

from java.util import Properties
from org.apache.flink.streaming.api.functions.source import SourceFunction
from org.apache.flink.streaming.api.collector.selector import OutputSelector
from org.apache.flink.api.common.serialization import SimpleStringSchema
from org.apache.flink.streaming.api.datastream import DataStream
from org.apache.flink.core.fs.FileSystem import WriteMode
from org.apache.flink.api.common.functions import FlatMapFunction, ReduceFunction, MapFunction
from org.apache.flink.streaming.api.functions.windowing import WindowFunction
from org.apache.flink.api.java.functions import KeySelector
from org.apache.flink.core.fs.FileSystem import WriteMode
import glob
import os
import sys
import json
import datetime
import time
import random
import math

directories=['/home/Ubuntu/flink-1.6.2/lib']
for directory in directories:
    for jar in glob.glob(os.path.join(directory,'*.jar')):
                sys.path.append(jar)

from org.apache.flink.streaming.connectors.kafka import 
                                        FlinkKafkaConsumer09

properties = Properties()
properties.setProperty("bootstrap.servers", "localhost:9092")
properties.setProperty("zookeeper.connect", "localhost:2181")
properties.setProperty("group.id", "testflink")

BREAKPOINTS={}

BREAKPOINTS['pm10']=[{'data': (0,54),    'aqi': (0,50)}, 
                     {'data': (55,154),  'aqi': (51,100)}, 
                     {'data': (155,254), 'aqi': (101,150)}, 
                     {'data': (255,354), 'aqi': (151, 200)}, 
                     {'data': (355,424), 'aqi': (201,300)}, 
                     {'data': (425,504), 'aqi': (301,400)}, 
                     {'data': (505,604), 'aqi': (401,500)}]

BREAKPOINTS['pm2_5']=[{'data': (0,15.4),     'aqi': (0,50)}, 
                     {'data': (15.5,40.4),   'aqi': (51,100)}, 
                     {'data': (40.5,65.4),   'aqi': (101,150)}, 
                     {'data': (65.5,150.4),  'aqi': (151, 200)}, 
                     {'data': (150.5,250.4), 'aqi': (201,300)}, 
                     {'data': (250.5,350.4), 'aqi': (301,400)}, 
                     {'data': (350.5,500.4), 'aqi': (401,500)}]

BREAKPOINTS['co']=  [{'data': (0.0,4.4),    'aqi': (0,50)}, 
                     {'data': (4.5,9.4),  'aqi': (51,100)}, 
                     {'data': (9.5,12.4), 'aqi': (101,150)}, 
                     {'data': (12.5,15.4), 'aqi': (151, 200)}, 
                     {'data': (15.5,30.4), 'aqi': (201,300)}, 
                     {'data': (30.5,40.4), 'aqi': (301,400)}, 
                     {'data': (40.5,50.4), 'aqi': (401,500)}]

BREAKPOINTS['so2']=[{'data': (0.000,0.034),    'aqi': (0,50)}, 
                     {'data': (0.035,0.144),  'aqi': (51,100)}, 
                     {'data': (0.145,0.224), 'aqi': (101,150)}, 
                     {'data': (0.225,0.304), 'aqi': (151, 200)}, 
                     {'data': (0.305,0.604), 'aqi': (201,300)}, 
                     {'data': (0.605,0.804), 'aqi': (301,400)}, 
                     {'data': (0.805,1.004), 'aqi': (401,500)}]

class Tokenizer(FlatMapFunction):
    def flatMap(self, value, collector):        
        data = json.loads(value)        
        collector.collect((data['stationID'], data['pm10'], 
                        data['pm2_5'], data['co'], data['so2']))

class Selector(KeySelector):
    def getKey(self, input):
        return input[0]

class ComputeAQI(WindowFunction):
    def apply(self, stationID, window, values, collector):
        total = 0
        count=0
        DATAKEYS=["pm10", "pm2_5", "co", "so2"]
        AQI=[]
        keyid=1
        now=int(time.time())

        for key in DATAKEYS:
            readings=[]
            for value in values:
                readings.append(value[keyid])

            readings_avg = sum(readings)/len(readings)
            C_p=readings_avg
            keyid=keyid+1

            for i in range(0,len(BREAKPOINTS[key])):
                BP_Lo = BREAKPOINTS[key][i]['data'][0]
                BP_Hi = BREAKPOINTS[key][i]['data'][1]
                I_Lo = BREAKPOINTS[key][i]['aqi'][0]
                I_Hi = BREAKPOINTS[key][i]['aqi'][1]
                if C_p>=BP_Lo and C_p<BP_Hi:
                    I_p = (I_Hi-I_Lo)*(C_p-BP_Lo)/(BP_Hi-BP_Lo)+I_Lo
                    result = int(math.ceil(I_p))
                    AQI.append((key, result))
                    break

        AQI_sorted = sorted(AQI, key=lambda x: x[-1],reverse=True)
        AQI_final = AQI_sorted[0][1]
        main_pollutant = AQI_sorted[0][0]
        collector.collect((stationID, AQI_final, 
                        str(now), str(main_pollutant)))


def main(factory):
    myConsumer = FlinkKafkaConsumer09("testflink", 
                            SimpleStringSchema(), properties)

    myConsumer.setStartFromLatest()

    env = factory.get_execution_environment()

    result = env.add_java_source(myConsumer)\
        .flat_map(Tokenizer())\
        .key_by(Selector())\
        .count_window(10, 10)\
        .apply(ComputeAQI())\
        .write_as_text("file:///home/Ubuntu/outstream.txt",
                         WriteMode.OVERWRITE)

    env.execute()