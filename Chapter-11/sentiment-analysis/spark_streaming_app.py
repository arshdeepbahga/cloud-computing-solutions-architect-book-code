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

import boto.dynamodb2 
from boto.dynamodb2.table import Table 
import boto.sqs 
from boto.sqs.message import Message 
import cPickle as pickle 
import json 
from pyspark import SparkContext 
from pyspark.streaming import StreamingContext 
from pyspark.streaming.kafka import KafkaUtils 
import random 
from random import randint 
import string 
import time 
import datetime 
from datetime import datetime as newdatetime 
import pytz 
 
# Create connection to DynamoDB service 
conn_dynamo = boto.dynamodb2.connect_to_region(REGION, 
   aws_access_key_id=ACCESS_KEY, 
   aws_secret_access_key=SECRET_KEY) 
 
# Retrieve handle to DynamoDB table 
table1=Table('tweets',connection=conn_dynamo) 
 
# Create connection to SQS service 
conn_sqs = boto.sqs.connect_to_region(REGION, 
   aws_access_key_id=ACCESS_KEY, 
   aws_secret_access_key=SECRET_KEY) 
 
# Retrieve handle to queue 
q1 = conn_sqs.get_all_queues(prefix='cricket') 
 
TERMS={} 
 
#-------- Load Sentiments Dict ---- 
sent_file = open('AFINN-111.txt') 
sent_lines = sent_file.readlines() 
for line in sent_lines: 
    s = line.split("\t") 
    TERMS$[$s$[$0$]$$]$ = s$[$1$]$ 
 
sent_file.close() 
 
 
#-------- Find Sentiment  ---------- 
def findsentiment(tweet): 
    sentiment=0.0 
 
    if tweet.has_key('text'): 
        text = tweet$[$'text'$]$         
        text=re.sub('$[$!@#$)(*=+/:;&%#|{},.?~]', '', text) 
        splitTweet=text.split() 
 
        for word in splitTweet: 
            if TERMS.has_key(word): 
                sentiment = sentiment+ float(TERMS$[$word$]$) 
 
    return sentiment 
 
#----Send analyzed Tweet to SQS and DynamoDB----     
def send_results(words): 
    tweet = json.loads(words) 
 
    sentimentScore = findsentiment(tweet)  
        
    datas={} 
    datas$[$'timestamp'$]$ =str(newdatetime.strptime(tweet$[$'created_at'$]$,  
        '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC))$[$:-6$]$ 
         
    datas$[$'id_str'$]$ = tweet$[$'id_str'$]$ 
    datas$[$'sentiment'$]$ = sentimentScore 
    datas$[$'tweet_name'$]$ = tweet$[$'user'$]$$[$'name'$]$ 
    datas$[$'tweet_text'$]$ = tweet$[$'text'$]$ 
    datas$[$'tweet_user_id'$]$ = tweet$[$'user'$]$$[$'screen_name'$]$ 
 
    p = pickle.dumps(json.loads(json.dumps(datas))) 
    m = Message() 
    m.set_body(p) 
    status = q1$[$0$]$.write(m) 
 
    item = table1.put_item(data=datas) 
 
 
 
# Create a local StreamingContext 
sc = SparkContext("local$[$2$]$", "NetworkWordCount") 
ssc = StreamingContext(sc, 5) 
 
cricket_kvs = KafkaUtils.createStream(ssc, '127.0.0.1',  
            "spark-streaming-consumer", {'Cricket': 1}) 
 
cricket_lines = cricket_kvs.map(lambda x: x$[$1$]$) 
 
cricket_lines.pprint() 
 
cricket_lines.foreachRDD(lambda rdd: rdd.foreach(send_results)) 
 
# Start the computation 
ssc.start()              
 
# Wait for the computation to terminate 
ssc.awaitTermination()
