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
import json
import datetime
import random
import boto3
AWS_KEY="<enter>"
AWS_SECRET="<enter>"
REGION="us-east-1"
kinesis_client = boto3.client('kinesis', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
def getData():
    messageJson={}
    station=random.randint(0,1)
    if station==0:
        messageJson['stationID']='ST102'
        messageJson['latitude']=33.717950
        messageJson['longitude']=-84.454540
    elif station==1:
        messageJson['stationID']='ST105'
        messageJson['latitude']=33.933337
        messageJson['longitude']=-84.357290
    now=datetime.datetime.utcnow()
    messageJson['timestamp']=int(time.time())
    messageJson['pm2_5']=random.randint(0,5004)/10.0
    messageJson['pm10']=random.randint(0,6040)/10.0
    messageJson['so2']=random.randint(0,1004)/1000.0
    messageJson['co']=random.randint(0,504)/100.0
    return messageJson

while True:        
    message = getData()
    messageJson = json.dumps(message)+"\n"    
    response = kinesis_client.put_record(StreamName='AirQualityData', 
                Data=messageJson, PartitionKey=messageJson)
    print('Published %s\n' % (messageJson))
    print response
    time.sleep(1)
