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

import paho.mqtt.client as mqtt 
import json 
import boto.sqs 
from boto.sqs.message import Message 
 
REGION="us-east-1" 
queue_name = 'sensordata' 
ACCESS_KEY = <Enter AWS Access Key> 
SECRET_KEY = <Enter Secret Key> 
 
conn = boto.sqs.connect_to_region(REGION,aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY) 
 
q = conn.get_all_queues(prefix=queue_name) 
 
 
def publish_to_sqs(data): 
    m = Message() 
    m.set_body(data) 
    status = q[0].write(m) 
    return status 
     
     
def on_connect(client, userdata, flags, rc): 
    print("Connected with result code "+str(rc)) 
    client.subscribe("$iot/test") 
 
def on_message(client, userdata, msg): 
    data = json.loads(msg.payload) 
    publish_to_sqs(data) 
 
 
client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 
 
client.connect("localhost", 1883, 60) 
 
client.loop_forever()
