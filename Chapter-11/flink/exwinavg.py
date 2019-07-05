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

from org.apache.flink.streaming.api.functions.source import SourceFunction
from org.apache.flink.api.common.functions import FlatMapFunction, ReduceFunction, MapFunction
from org.apache.flink.streaming.api.functions.windowing import WindowFunction
from org.apache.flink.api.java.functions import KeySelector
from org.apache.flink.core.fs.FileSystem import WriteMode
import json
import datetime
import time
import random

class Generator(SourceFunction):
    def __init__(self, num_iters=1000):
        self._running = True
        self._num_iters = num_iters

    def run(self, ctx):
        counter = 0
        while self._running and counter < self._num_iters:
            self.do(ctx)
            counter += 1

    def do(self, ctx):
        messageJson={}
        station=random.randint(0,1)
        if station==0:
            messageJson['stationID']='ST102'
        elif station==1:
            messageJson['stationID']='ST105'
        
        now=datetime.datetime.utcnow()
        messageJson['timestamp']=int(time.time())
        messageJson['pm2_5']=random.randint(0,5004)/10.0
        messageJson['pm10']=random.randint(0,6040)/10.0
        messageJson['so2']=random.randint(0,1004)/1000.0
        messageJson['co']=random.randint(0,504)/100.0
        
        ctx.collect(json.dumps(messageJson))

    def cancel(self):
        self._running = False

class Tokenizer(FlatMapFunction):
    def flatMap(self, value, collector):        
        data = json.loads(value)        
        collector.collect((data['stationID'], data['pm10']))

class Selector(KeySelector):
    def getKey(self, input):
        return input[0]

class ComputeAvg(WindowFunction):
    def apply(self, stationID, window, values, collector):
        total=0
        count=0
        for value in values:
            total=total+value[1]
            count=count+1
        avg=total/count
        collector.collect((stationID, avg))

def main(factory):
    env = factory.get_execution_environment()
    result = env.create_python_source(Generator(num_iters=100)) \
        .flat_map(Tokenizer()) \
        .key_by(Selector()) \
        .count_window(10, 10)\
        .apply(ComputeAvg())\
        .write_as_text("file:///home/Ubuntu/outstream.txt", 
                        WriteMode.OVERWRITE)       
    env.execute()
