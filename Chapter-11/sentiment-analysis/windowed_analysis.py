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

from pyspark import SparkContext  
from pyspark.streaming import StreamingContext  
from pyspark.streaming.kafka import KafkaUtils  
 
#Load Sentiments Dictionary 
sent_file = open('AFINN-111.txt') 
sent_lines = sent_file.readlines() 
for line in sent_lines: 
    s = line.split("\t") 
    TERMS[s[0]] = s[1] 
sent_file.close() 
 
 
def findsentiment(tweet): 
    sentiment=0.0 
    if tweet.has_key('text'): 
        text = tweet['text'] 
        splitTweet=text.split() 
         
        for word in splitTweet: 
            if TERMS.has_key(word): 
                sentiment = sentiment+ float(TERMS[word]) 
 
    return sentiment 
 
def analyzeData(data): 
    tweet = json.loads(data) 
    sentiment= findsentiment(tweet) 
    if sentiment>0: 
        return ("Positive", 1) 
    elif sentiment<0: 
        return ("Negative", 1) 
    else: 
        return ("Neutral", 1) 
         
sc = SparkContext(appName="SentimentAnalysis")  
scc = StreamingContext(sc,1)  
  
#Replace with DNS of instance running Zookeeper  
zkQuorum = "ip-172-31-33-135.ec2.internal:2181"  
topic = "tweets"  
  
kvs = KafkaUtils.createStream(ssc, zkQuorum,   
        "spark-streaming-consumer", {topic:1})  
tweets = kvs.map(lambda x: x[1])  
  
sentiments = tweets.map(analyzeData)  
 
windowedSentiments = sentiments.reduceByKeyAndWindow(lambda x,  
                    y: x + y, lambda x, y: x - y, 30, 10) 
  
windowedSentiments.pprint()  
  
ssc.start()  
ssc.awaitTermination()
