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

INSTANCE_TYPE="db.t2.micro"
ID = "MySQL-db-instance"
USERNAME = 'root'
PASSWORD = 'password'
DB_PORT = 3306
DB_SIZE = 5
DB_ENGINE = 'mysql'
DB_NAME = 'mytestdb'
SECGROUP_ID="sg-1f25617b"

print "Connecting to RDS"

rds = boto3.client('rds', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

print "Creating an RDS instance"

response = rds.create_db_instance(DBName=DB_NAME, 
            DBInstanceIdentifier=ID, 
            AllocatedStorage=DB_SIZE,
            DBInstanceClass=INSTANCE_TYPE, 
            Engine=DB_ENGINE,
            MasterUsername=USERNAME,
            MasterUserPassword=PASSWORD,
            VpcSecurityGroupIds=[
                SECGROUP_ID,
            ],
            Port=DB_PORT)
    
print response
print "Waiting for instance to be up and running"
sleep(30)
response = rds.describe_db_instances(DBInstanceIdentifier=ID)
status = response['DBInstances'][0]['DBInstanceStatus']
    
while not status == 'available':
    sleep(10)
    response = rds.describe_db_instances(DBInstanceIdentifier=ID)
    status = response['DBInstances'][0]['DBInstanceStatus']
    print "Status: "+str(status)

if status == 'available':
    response = rds.describe_db_instances(DBInstanceIdentifier=ID)
    print "\nRDS Instance is now running. Instance details are:"
    print "Intance ID: " + \
        str(response['DBInstances'][0]['DBInstanceIdentifier'])
    print "Intance State: " + \
        str(response['DBInstances'][0]['DBInstanceStatus'])
    print "Instance Type: " + \
        str(response['DBInstances'][0]['DBInstanceClass'])
    print "Engine: " + str(response['DBInstances'][0]['Engine'])
    print "Allocated Storage: " + \
    str(response['DBInstances'][0]['AllocatedStorage'])
    print "Endpoint: " + str(response['DBInstances'][0]['Endpoint'])


