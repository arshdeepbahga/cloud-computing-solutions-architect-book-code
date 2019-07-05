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
from datetime import date 
import time 
import datetime 
import boto.dynamodb2 
from boto.dynamodb2.table import Table 
import json 
import re 
 
ACCESS_KEY="<Enter>" 
SECRET_KEY="<Enter>" 
REGION="us-east-1" 
 
 
#Connect to DynamoDB 
conn = boto.dynamodb2.connect_to_region(REGION, 
            aws_access_key_id=ACCESS_KEY, 
            aws_secret_access_key=SECRET_KEY) 
 
TERMS={} 
#-------- Load Sentiments Dict ---- 
sent_file = open('AFINN-111.txt') 
sent_lines = sent_file.readlines() 
for line in sent_lines: 
    s = line.split("\t") 
    TERMS[s[0]] = s[1] 
 
sent_file.close() 
 
    
 
#-------- Find Sentiment  ---------- 
def findsentiment(tweet): 
    sentiment=0.0 
     
    if tweet.has_key('text'): 
        text = tweet['text'] 
        text=re.sub('[!@#$)(*<>=+/:;&%#|{},.?~]', '', text) 
        splitTweet=text.split() 
         
        for word in splitTweet: 
            if TERMS.has_key(word): 
                sentiment = sentiment+ float(TERMS[word]) 
 
    return sentiment 
 
def analyzeData(data): 
    #Add your code for data analysis here 
    tweet = json.loads(data) 
    sentiment= findsentiment(tweet) 
    return sentiment 
 
class MyBolt(storm.BasicBolt): 
    def process(self, tup): 
        now = datetime.datetime.now() 
        data = tup.values[0] 
         
        output = analyzeData(data) 
        tweet=json.loads(data) 
        today = date.today() 
        timestampp=now.strftime("%H:%M:%S") 
        #Store analyzed results in DynamoDB 
        table=Table('twittersentiment',connection=conn) 
        item = table.put_item(data={ 
                              'date':str(today), 
                              'timestamp':str(timestampp), 
                              'tweet': tweet['text'], 
                              'sentiment':str(output) 
                              },overwrite=True) 
 
 
MyBolt().run()
