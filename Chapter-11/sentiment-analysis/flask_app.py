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

from flask import Flask, jsonify, abort, request, make_response, url_for 
from flask.ext.cors import CORS 
import sqlite3 
import json 
import random   
from random import randint 
import string 
import datetime 
import boto.sqs 
from boto.sqs.message import Message 
import cPickle as pickle 
from time import sleep 
 
app = Flask(__name__, static_url_path="") 
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) 
 
#Create connection to SQS service 
conn_sqs = boto.sqs.connect_to_region(REGION, 
   aws_access_key_id=ACCESS_KEY, 
   aws_secret_access_key=SECRET_KEY) 
 
# Retrieve handle to queue 
q1 = conn_sqs.get_all_queues(prefix='weather') 
 
@app.route('/api/update', methods=$[$'GET'$]$) 
def get_updates(): 
    topics = {} 
    tweets = $[$$]$ 
    flag = False 
    data1 = {'empty': 'null'} 
     
    count = q1$[$0$]$.count() 
    if count > 0: 
        m = q1$[$0$]$.read() 
        bod = m.get_body() 
        data1 = pickle.loads(str(bod)) 
        q1$[$0$]$.delete_message(m) 

    topics$[$'Cricket'$]$ = data1 
    print topics 
    return jsonify(topics) 
 
 
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0')
