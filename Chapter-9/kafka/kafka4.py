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

import time 
import datetime 
from kafka import KafkaClient, KeyedProducer,  
from kafka import HashedPartitioner, RoundRobinPartitioner 
 
kafka = KafkaClient("localhost:6667") 
 
#Default partitioner is HashedPartitioner 
producer = KeyedProducer(kafka) 
producer.send("test", "key1", "Test message with key1") 
producer.send("test", "key2", "Test message with key2") 
 
#Using RoundRobinPartitioner 
producer = KeyedProducer(kafka, partitioner=RoundRobinPartitioner) 
producer.send("test", "key3", "Test message with key3") 
producer.send("test", "key4", "Test message with key4") 
