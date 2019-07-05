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
from org.apache.flink.core.fs.FileSystem import WriteMode
from org.apache.flink.api.common.functions import FlatMapFunction
import glob
import os
import sys
import json
import random
import re

directories=['/home/Ubuntu/flink-1.6.2/lib']
for directory in directories:
    for jar in glob.glob(os.path.join(directory,'*.jar')):
                sys.path.append(jar)

from org.apache.flink.streaming.connectors.twitter import TwitterSource

properties = Properties()
properties.setProperty(TwitterSource.CONSUMER_KEY, "<enter>")
properties.setProperty(TwitterSource.CONSUMER_SECRET, "<enter>")
properties.setProperty(TwitterSource.TOKEN, "<enter>")
properties.setProperty(TwitterSource.TOKEN_SECRET, "<enter>")

#----- Load Sentiments Dict ---
TERMS={}
sent_file = open('AFINN-111.txt')
sent_lines = sent_file.readlines()
for line in sent_lines:
    s = line.split("\t")
    TERMS[s[0]] = s[1]
    sent_file.close()

def findsentiment(text):
    sentiment=0.0
    try:
        text=re.sub('[!@#$)(*<>=+/:;&%#|{},.?]', '', text)
        splitTweet=text.split()
        for word in splitTweet:
            if TERMS.has_key(word):
                sentiment = sentiment+ float(TERMS[word])
    except:
        pass
    return sentiment

class ComputeSentiment(FlatMapFunction):
    def flatMap(self, value, collector):        
        data = json.loads(value)     
        sentiment=findsentiment(data['text'])   
        collector.collect((data['timestamp_ms'], 
                            data['text'], sentiment))

def main(factory):
    myConsumer = TwitterSource(properties)
    env = factory.get_execution_environment()

    result = env.add_java_source(myConsumer)\
        .flat_map(ComputeSentiment()) \
        .write_as_text("file:///home/Ubuntu/outstream.txt", 
                            WriteMode.OVERWRITE)
    env.execute()


