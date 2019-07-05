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

from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler 
from tweepy import Stream 
from random import randrange 
import time 
import datetime 
from kafka import KafkaProducer 
import httplib 
import json 
 
#Variables that contains the user credentials to access Twitter API  
access_token = "<enter>" 
access_token_secret = "<enter>" 
consumer_key = "<enter>" 
consumer_secret = "<enter>" 
 
#List of keywords to filter  
keywords_list = $[$'cricket'$]$ 
 
#Connect to Kafka 
producer = KafkaProducer(bootstrap_servers=$[$'127.0.0.1:6667'$]$) 
   
#This is a function publishes data to a Kafka topic 
def publish(data): 
    tweet = json.loads(data) 
    if("retweeted" in tweet.keys()): 
    if(tweet$[$'retweeted'$]$ == False): 
        print tweet$[$'text'$]$ 
         
        #Send tweet to a topic named Cricket 
        producer.send('Cricket', data.encode("utf")) 
         
#This is a basic listener that just prints received tweets to stdout. 
class StdOutListener(StreamListener): 
    def on_data(self, data): 
    publish(data) 
    return True 
     
    def on_error(self, status): 
        print status 
     
if __name__ == '__main__': 
    #This handles Twitter authetification and 
    #the connection to Twitter Streaming API 
    l = StdOutListener() 
    auth = OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    while True: 
        try: 
            stream = Stream(auth, l) 
        stream.filter(track=keywords_list,languages =$[$'en'$]$) 
 
        except httplib.IncompleteRead: 
            print "Incomplete Read!!!!" 
            pass
