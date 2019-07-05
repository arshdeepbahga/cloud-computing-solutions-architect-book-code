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
import time 
import datetime 
from kafka.client import KafkaClient 
from kafka.producer import SimpleProducer 
 
#Connect to Kafka 
client = KafkaClient("ip-172-31-60-0.ec2.internal:6667") 
producer = SimpleProducer(client) 
 
 
#Get Twitter API keys from Twitter developer account 
access_token = "<Enter>" 
access_token_secret = "<Enter>" 
consumer_key = "<Enter>" 
consumer_secret = "<Enter>" 
 
 
def publish(data): 
    producer.send_messages('mytopic', data.encode()) 
     
     
class StdOutListener(StreamListener): 
 
    def on_data(self, data): 
        publish(data) 
 
    def on_error(self, status): 
        print status 
 
if __name__ == '__main__': 
    print 'Listening...' 
    #This handles Twitter authetification and  
    #the connection to Twitter Streaming API 
    #sets callback on data 
    l = StdOutListener() 
    auth = OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    stream = Stream(auth, l) 
 
    #This line filter Twitter Streams to capture data by the keywords 
    stream.filter(track=['basketball'])
