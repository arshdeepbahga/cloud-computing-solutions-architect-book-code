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
    code=event['body-json']['code']
    result=False
    message=""
    response={}
    returndata={} 
    try:
        response = cognitoclient.confirm_sign_up(
                ClientId=CLIENT_ID,
                Username=username,
                ConfirmationCode=code
            )
        result=True
        message="User confirmed"
    except ClientError as e:
        message="Error in confirming email"
        if e.response['Error']['Code'] == 'UserNotFoundException':
            result=False
            message="Can't Find user by Email"
        if e.response['Error']['Code'] == 'CodeMismatchException':
            result=False
            message="User Code Mismatch"
        if e.response['Error']['Code'] == 'ParamValidationError':
            result=False
            message="Param Validation Error"
        if e.response['Error']['Code'] == 'ExpiredCodeException':
            result=False
            message="Expired Code"
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            result=False
            message="User already confirmed"
    
    returndata['result']=result
    returndata['message']=message
    
    return {
        "statusCode": 200,
        "body": json.dumps(returndata)
    }