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

import pika 
from time import time 
import json 
import pickle, re, os, urllib, urllib2 
from datetime import datetime 
from random import randrange 
import time 
import datetime 
 
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) 
channel = connection.channel() 
 
channel.queue_declare(queue='test') 
 
while True: 
    data = str(randrange(0,60))  + ',' + str(randrange(0,100)) + ',' + str(randrange(5000,12000)) + ',' + str(randrange(50,350)) 
              
    ts=time.time() 
    timestamp = 
    datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 
 
    msg={'timestamp': timestamp, 'data': data} 
    print msg 
     
    channel.basic_publish(exchange='', 
                      routing_key='test', 
                      body=json.dumps(msg)) 
 
    print data 
    time.sleep(1)
