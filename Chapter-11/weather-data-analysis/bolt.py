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

import storm 
import json 
import re 
from cassandra.cluster import Cluster 
import blist 
from sklearn import svm 
from sklearn.externals import joblib 
import datetime 
#----------- Load Clf files ----------- 
svmFog = joblib.load('svmFog.pkl') 
svmHaze = joblib.load('svmHaze.pkl') 
 
#-------- Connect to Cassandra -------- 
cluster = Cluster(['127.0.0.1']) 
session = cluster.connect('predictions')  
 
def analyzeData(data): 
    fog_predict = svmFog.predict(data) 
    haze_predict = svmHaze.predict(data) 
    return [str(fog_predict[0]), str(haze_predict[0])] 
 
class SensorBolt(storm.BasicBolt): 
    def process(self, tup): 
        data = tup.values[0] 
 
        output = analyzeData(data) 
        result = "Result: "+ str(output) 
        timestamp= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
 
        #Store analyzed results in Cassandra 
        session.execute( 
        """ 
        INSERT INTO data(timestamp, fog_prediction, haze_prediction) 
        VALUES (%s, %s, %s) 
        """, 
        (timestamp, output[0], output[1]) 
        ) 
 
        storm.emit([result]) 
 
SensorBolt().run()
