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

import random 
import sys 
import uuid 
from cassandra.cluster import Cluster 
from pyspark import SparkContext 
from pyspark.streaming import StreamingContext 
from pyspark.streaming.kafka import KafkaUtils 
from operator import add 
from kafka.client import KafkaClient 
from kafka.consumer import SimpleConsumer 
from kafka.producer import SimpleProducer 
from pyspark.sql import SQLContext 
from pyspark.sql.types import Row, StructField,  
    StructType, StringType, IntegerType 
import datetime 
from datetime import timedelta 
 
 
timestamp = datetime.datetime.utcnow() 
client = KafkaClient('ip-172-31-39-49.ec2.internal:6667') 
producer = SimpleProducer(client) 
 
cluster = Cluster() 
session = cluster.connect('test') 
baseRate = 2 
totalSlots = 500.0 
 
 
def printel(x): 
    global timestamp      
    l = x.collect() 
    if len(l) !=3: 
    return 
    print l 
    for lot,cars in l: 
        lotid= lot.strip("'") 
       occrate = ( cars / totalSlots)  * 100 
     
      if occrate > 100: 
        occrate = 100 
             price = -1 
        else:        
            price = 2 + (occrate/100) * 20 
 
        session.execute("INSERT INTO smartpark (key,lotid,occrate,time,price) VALUES (%s,%s,%s,%s,%s)", [uuid.uuid4(),int(lotid),occrate,str(timestamp)[:-7],price]) 
        seconds = random.randint(1800,2400) 
        timestamp = timestamp + datetime.timedelta(0,seconds) 
     
 
sc = SparkContext(appName="SmartParking") 
sqlContext = SQLContext(sc) 
ssc = StreamingContext(sc, 0.250) 
 
# Replace with DNS of instance running Zookeeper 
zkQuorum = "ip-172-31-39-49.ec2.internal:2181" 
topic = "smartparking" 
 
kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1}) 
lines = kvs.map(lambda x: x[1]) 
 
lines = lines.map(lambda line: line.encode('ascii','ignore')) 
lines = lines.map(lambda line: line.split(",")) 
lines = lines.map(lambda line: (line[0][1:] ,1  
        if line[3][2:-2] == "True" else 0)).reduceByKey(add) 
         
lines.foreachRDD(lambda rdd: printel(rdd)) 
ssc.start() 
ssc.awaitTermination()
