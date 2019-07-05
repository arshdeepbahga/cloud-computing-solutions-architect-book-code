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

import boto.sqs 
from boto.sqs.message import Message 
import boto.dynamodb2 
from boto.dynamodb2.table import Table 
import cPickle as pickle 
import time 
import datetime 
import json 
from flask import Flask, jsonify, abort,  
from flask import request, make_response, url_for 
          
app = Flask(__name__, static_url_path="") 
 
ACCESS_KEY = <Enter AWS Access Key> 
SECRET_KEY = <Enter Secret Key> 
REGION="us-east-1" 
queue_name = 'sensordata' 
table_name = 'sensordata' 
 
#Connect to AWS SQS 
conn = boto.sqs.connect_to_region(REGION,aws_access_key_id=ACCESS_KEY, 
 aws_secret_access_key=SECRET_KEY) 
 
q = conn.get_all_queues(prefix=queue_name) 
 
#Connect to AWS DynamoDB 
conn_dynamo = boto.dynamodb2.connect_to_region(REGION, 
    aws_access_key_id=ACCESS_KEY, 
    aws_secret_access_key=SECRET_KEY) 
 
table=Table(table_name,connection=conn_dynamo) 
 
#Publishes data to SQS 
def publish_to_sqs(data): 
    m = Message() 
    m.set_body(data) 
    status = q[0].write(m) 
    return status 
 
#Writes data to DynamoDB table 
def publish_to_dynamo(datadir): 
    item = table.put_item(data=datadir) 
     
@app.errorhandler(400) 
def bad_request(error): 
    return make_response(jsonify({'error': 'Bad request'}), 400) 
 
@app.errorhandler(404) 
def not_found(error): 
    return make_response(jsonify({'error': 'Not found'}), 404) 
     
 
@app.route('/api/data', methods=['POST']) 
def post_data(): 
    data = json.loads(request.data)         
     
    publish_to_sqs(pickle.dumps(data)) 
     
    publish_to_dynamo(data) 
     
    return jsonify({'result': 'true'}), 201 
     
if __name__ == '__main__': 
    app.run(debug=True) 
