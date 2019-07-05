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
import boto3  
import time
import datetime

REGION="us-east-1"
dynamodb = boto3.resource('dynamodb',region_name=REGION)
table = dynamodb.Table('PhotoGallery')

def lambda_handler(event, context):
    username=event['body-json']['username']
    title=event['body-json']['title']
    description=event['body-json']['description']
    tags=event['body-json']['tags']
    uploadedFileURL=event['body-json']['uploadedFileURL']    
    ts=time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).\
                    strftime('%Y-%m-%d %H:%M:%S')
    photoID=str(int(ts*1000))
    
    table.put_item(
    Item={                        
            "PhotoID": photoID,
            "Username": username,
            "CreationTime": timestamp,
            "Title": title,
            "Description": description,
            "Tags": tags,
            "URL": uploadedFileURL            
        }
    )
                
    return {
        "statusCode": 200,
        "body": json.dumps(photoID)
    }
    
    
    
