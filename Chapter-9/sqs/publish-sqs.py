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

import boto3
from random import randint
import time
import datetime
import json

AWS_KEY="<enter>"
AWS_SECRET="<enter>"
REGION="us-east-1"
QUEUE_NAME='<enter>'

sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)

def getData():
    ts=time.time()
    timestamp=int(time.time())
    temp = randint(0,100)
    humidity = randint(0,100)
    co2 = randint(50,500)
    light = randint(0,10000)
    data = {"timestamp": timestamp, "temperature": temp, 
            "humidity": humidity , "co2": co2, "light": light}
    return data

def publish(data):
    #For Standard Queue
    queue.send_message(MessageBody=json.dumps(data))

    #For FIFO Queue provide MessageDeduplicationId and MessageGroupId
    #queue.send_message(MessageBody=json.dumps(data), 
    #MessageDeduplicationId=str(data['timestamp']), MessageGroupId="1")
    
while True:
    data = getData()
    print data
    publish(data)
    time.sleep(1)
                

