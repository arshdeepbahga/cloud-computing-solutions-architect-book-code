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
import json
import boto3
import pytz
from dateutil.tz import tzlocal
AWS_KEY="<enter>"
AWS_SECRET="<enter>"
REGION="us-east-1"
kinesis_client = boto3.client('kinesis', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

response = kinesis_client.describe_stream( StreamName='AirQualityData')

if response['StreamDescription']['StreamStatus'] == 'ACTIVE':
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']
    print shard_id

while True:
    response = kinesis_client.get_shard_iterator(
                            StreamName='AirQualityData', 
                            ShardId=shard_id, 
                            ShardIteratorType='LATEST')
    shard_iterator = response['ShardIterator']
    response = kinesis_client.get_records(ShardIterator=shard_iterator)
    for record in response['Records']:
        print record            
    shard_iterator = response['NextShardIterator']