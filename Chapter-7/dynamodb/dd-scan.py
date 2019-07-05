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
from boto3.dynamodb.conditions import Key, Attr

AWS_KEY="<enter>"
AWS_SECRET="<enter>"
REGION="us-east-1"

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
client = boto3.client('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

table = dynamodb.Table('customers')

#Describe table
response = client.describe_table(TableName='customers')
print response

#Scan table
response=table.scan()
items = response['Items']
for item in items:
    print item

#Scan table with filter
response = table.scan(FilterExpression=Attr('country').eq('India'))
items = response['Items']
for item in items:
    print item

#Scan table with filters
response = table.scan(
	FilterExpression=Attr('createdAt').between('2012-03-26T00:00:00-00:00',
					'2013-03-26T00:00:00-00:00'))
items = response['Items']
for item in items:
    print item

#Query table with partition key
response = table.query(
	KeyConditionExpression=Key('customerID').eq('1623072020799'))
items = response['Items']
for item in items:
    print item