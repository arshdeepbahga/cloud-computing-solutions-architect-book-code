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

AWS_KEY="<enter>"
AWS_SECRET="<enter>"
REGION="us-east-1"

print "Connecting to EC2"
ec2 = boto3.client('ec2', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

response = ec2.describe_instances()
for instance in response['Reservations'][0]['Instances']:
    print "Intance Type: " + str(instance['InstanceType'])
    print "Intance State: " + str(instance['State']['Name'])
    print "Intance Launch Time: " + str(instance['LaunchTime'])
    print "Intance Public DNS: " + str(instance['PublicDnsName'])
    print "Intance Private DNS: " + str(instance['PrivateDnsName'])
    print "Intance IP: " + str(instance['PublicIpAddress'])
    print "Intance Private IP: " + str(instance['PrivateIpAddress'])



