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

from random import randrange 
import time 
import datetime 
from kafka.client import KafkaClient 
from kafka.consumer import SimpleConsumer 
from kafka.producer import SimpleProducer 
import csv 
import json 
import time 
 
#Connect to Kafka 
#change to private DNS 
client = KafkaClient("127.0.0.1:6667") 
producer = SimpleProducer(client) 
 
def is_number(s): 
    try: 
        float(s) 
    except ValueError: 
        return False 
    return True 
 
def sysTest(filename): 
    f = open(filename) 
    csv_f = csv.reader(f) 
    tList=[] 
    tClass=[] 
    counter=0 
    for row in csv_f: 
        new_list=[] 
        if counter < 2: 
            counter=counter+1 
            continue 
        for item in row: 
            if not(is_number(item)): 
                continue 
            new_list.append(float(item)) 
        #print new_list 
        if len(new_list)!=5: 
            continue 
        dataSend=json.dumps(new_list).encode('utf-8') 
        producer.send_messages('weather',dataSend) 
        time.sleep(5) 
        print dataSend 
        print type(dataSend) 
    f.close() 
 
 
if __name__ == '__main__': 
    print 'Publishing...' 
    sysTest('PositiveFog.csv') 
    sysTest('PositiveHaze.csv') 
    sysTest('NegativeFogHaze.csv') 
