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

#Data format: 
#"2014-06-25 10:47:44",26,36,2860,274 
 
from pyspark import SparkContext 
from pyspark.streaming import StreamingContext 
from pyspark.streaming.kafka import KafkaUtils 
 
sc = SparkContext(appName="FilterSensorData") 
scc = StreamingContext(sc,1) 
 
#Replace with DNS of instance running Zookeeper 
zkQuorum = "ip-172-31-33-135.ec2.internal:2181" 
topic = "forestfire" 
 
kvs = KafkaUtils.createStream(ssc, zkQuorum,  
        "spark-streaming-consumer", {topic:1}) 
lines = kvs.map(lambda x: x[1]) 
 
splitlines = lines.map(lambda line: line.split(',')) 
filteredlines = splitlines.filter(lambda line: int(line[1])>20 and  
        int(line[2])>20 and int(line[3])>6000  
        and int(line[4])>200) 
 
filteredlines.pprint() 
 
ssc.start() 
ssc.awaitTermination()
