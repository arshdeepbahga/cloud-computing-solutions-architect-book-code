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
from botocore.exceptions import ClientError

REGION="us-east-1"
USER_POOL_ID="<enter>"
CLIENT_ID="<enter>"

cognitoclient = boto3.client('cognito-idp', region_name=REGION)
                            
def lambda_handler(event, context):
    username=event['body-json']['username']
    password=event['body-json']['password']
    result=False
    message=""
    response={}
    returndata={} 
    userdata={}
    try:
        response = cognitoclient.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
    except ClientError as e:
        message="Error in logging in"
        if e.response['Error']['Code'] == 'UserNotFoundException':
            result=False
            message=="Can't Find user by Email"
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            result=False
            message="Incorrect username or password"
        if e.response['Error']['Code'] == 'UserNotConfirmedException':
            result=False
            message="User is not confirmed"

    if 'ResponseMetadata' in response:
        if response['ResponseMetadata']['HTTPStatusCode']==200:        
            result=True
            message="Login successful"
            response = cognitoclient.admin_get_user(
                UserPoolId=USER_POOL_ID,
                Username=username
            )
            for item in response['UserAttributes']:
                if item['Name']=='name':
                    userdata['name']=item['Value']
                elif item['Name']=='email':
                    userdata['email']=item['Value']
                elif item['Name']=='email_verified':
                    userdata['email_verified']=item['Value']
        else:
            return False
            message="Something went wrong"
            
    userdata['username']=username
    returndata['result']=result
    returndata['message']=message
    returndata['userdata']=userdata
    
    return {
        "statusCode": 200,
        "body": json.dumps(returndata)
    }