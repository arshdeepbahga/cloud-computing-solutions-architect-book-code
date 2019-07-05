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

import json
import re
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from random import randint
import time
import datetime
import csv

AWS_KEY="<enter>"
AWS_SECRET="<enter>"
REGION="us-east-1"
ES_ENDPOINT="<enter-cluster-endpoint>"
ES_INDEX="books"

# Get proper credentials for ES auth
awsauth = AWS4Auth(AWS_KEY, AWS_SECRET, REGION, 'es')
                       
# Connect to ES
es = Elasticsearch(
    [ES_ENDPOINT],
    http_auth=awsauth,
    use_ssl=True,
    port=443,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

print("Cluster info:")
print(es.info())

def insert_document(es, record):
    try:
        doc = json.dumps(record)    
        print("New document to Index:")
        print(doc)

        es.index(index=ES_INDEX,
                 body=doc,
                 id=record['asin'],
                 doc_type=ES_INDEX,
                 refresh=True)
    except:
        pass


reader = csv.reader(open('book32-listing.csv','r'))
header=reader.next()

for row in reader:    
    data = {"asin": row[0], "filename": row[1], 
            "image_url": row[2], "title": row[3], 
            "author": row[4], "category_id": int(row[5]), 
            "category": row[6]}

    insert_document(es, data)
