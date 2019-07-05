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

import feedparser 
import threading 
import sys 
import time 
import subprocess 
from datetime import datetime 
 
refresh_time = 300 #in seconds 
 
rss_feeds = [ 
('http://rss.cnn.com/rss/cnn_topstories.rss', 'CNN'), 
('http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'The New York Times'), 
('http://www.wsj.com/xml/rss/3_7085.xml', 'Wall Street Journal'), 
('http://www.news.gatech.edu/rss/all', 'Georgia Tech News')] 
 
csv_file = open("Output.csv","a") 
 
sentiments={} 
file = open('AFINN-111.txt') 
lines = file.readlines() 
for line in lines: 
    s = line.split("\t") 
    sentiments[s[0]] = s[1].strip() 
file.close() 
 
def get_sentiment_score(phrase): 
    phrase = phrase.strip() 
    total = 0.0 
    for word in phrase.split(): 
        word = word.lower() 
        for char in '[!@#$)(*<>=+/:;&%#|{},.?~]':
            word = word.replace(char,'') 
        if word in list(sentiments): 
            total = total + float(sentiments[word]) 
    return total 
 
     
last_round_headlines = [] 
this_round_headlines = [] 
 
def get_headlines(rss_feed): 
    feed = feedparser.parse(rss_feed[0]) 
    for entry in feed.entries: 
        title = entry.title.encode('utf-8') 
        this_round_headlines.append(title) 
        if title not in last_round_headlines: 
            score = get_sentiment_score(title) 
            title = title.replace(',','') 
            #Format: # score, title, link, source, timestamp 
            to_print = "" + str(score) + ", " + title + ", " + entry.link.encode('utf-8') + ", " + rss_feed[1] +  ", " + str(datetime.now())  
            csv_file.write(to_print) 
             
         
 
while True: 
    for rss_feed in rss_feeds: 
        t = threading.Thread(target=get_headlines, args = (rss_feed,)) 
        t.start() 
    time.sleep(refresh_time) 
    last_round_headlines = list(this_round_headlines) 
    this_round_headlines = list()
