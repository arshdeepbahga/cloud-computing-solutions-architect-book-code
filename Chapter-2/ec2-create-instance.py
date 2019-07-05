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
from time import sleep

AWS_KEY="<enter>"
AWS_SECRET="<enter>"
REGION="us-east-1"
AMI_ID = "ami-80861296"
EC2_KEY_HANDLE = "cloud"
INSTANCE_TYPE="t2.nano"
SECGROUP_ID="sg-1f25617b"

print "Connecting to EC2"

ec2 = boto3.client('ec2', aws_access_key_id=AWS_KEY,
              aws_secret_access_key=AWS_SECRET,
              region_name=REGION)

print "Launching instance with AMI-ID %s, with keypair %s, \
     instance type %s, security group \
     %s"%(AMI_ID,EC2_KEY_HANDLE,INSTANCE_TYPE,SECGROUP_ID)

response =  ec2.run_instances(ImageId=AMI_ID, 
               KeyName=EC2_KEY_HANDLE, 
               InstanceType=INSTANCE_TYPE,
               SecurityGroupIds = [ SECGROUP_ID, ],
               MinCount=1,
               MaxCount=1)

print response
Instance_ID=response['Instances'][0]['InstanceId']

print "Waiting for instance to be up and running"

response = ec2.describe_instances(InstanceIds=[Instance_ID])
status=response['Reservations'][0]['Instances'][0]['State']['Name']
print "Status: "+str(status)

while status == 'pending':
  sleep(10)
  response = ec2.describe_instances(InstanceIds=[Instance_ID])
  status=response['Reservations'][0]['Instances'][0]['State']['Name']
  print "Status: "+str(status)

if status == 'running':
  response = ec2.describe_instances(InstanceIds=[Instance_ID])
  print "\nInstance is now running. Instance details are:"
  print "Intance Type: " + \
    str(response['Reservations'][0]['Instances'][0]['InstanceType'])
  print "Intance State: " + \
    str(response['Reservations'][0]['Instances'][0]['State']['Name'])
  print "Intance Launch Time: " + \
    str(response['Reservations'][0]['Instances'][0]['LaunchTime'])
  print "Intance Public DNS: " + \
    str(response['Reservations'][0]['Instances'][0]['PublicDnsName'])
  print "Intance Private DNS: " + \
    str(response['Reservations'][0]['Instances'][0]['PrivateDnsName'])
  print "Intance IP: " + \
    str(response['Reservations'][0]['Instances'][0]['PublicIpAddress'])
  print "Intance Private IP: " + \
    str(response['Reservations'][0]['Instances'][0]['PrivateIpAddress'])



