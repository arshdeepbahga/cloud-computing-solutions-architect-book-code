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

import os
import boto.s3

conn = boto.connect_s3(aws_access_key_id='<enter>',
     aws_secret_access_key='<enter>')

def percent_cb(complete, total):
    print ('.')

def upload_to_s3_bucket_path(bucketname, path, filename):
	mybucket = conn.get_bucket(bucketname)
	fullkeyname=os.path.join(path,filename)
	key = mybucket.new_key(fullkeyname)
	key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)
	#key.make_public(recursive=False)

def upload_to_s3_bucket_root(bucketname, filename):
	mybucket = conn.get_bucket(bucketname)
	key = mybucket.new_key(filename)
	key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)

def getuserfiles(bucketname,username):
	mybucket = conn.get_bucket(bucketname)
	keys = mybucket.list(username)
	totalsize=0.0
	userfiles = {}
	for key in keys:
		value=[]
		#value.append(key.name)
		filename = key.name
		filename=filename.replace(username+'/media/','')
		value.append(key.last_modified)
		keysize = float(key.size)/1000.0
		value.append(str(keysize))
		userfiles[filename]=value
		totalsize = totalsize + float(key.size)
	totalsize = totalsize/1000000.0
	return userfiles,totalsize

def delete_from_s3(bucketname, username,filename):
	mybucket = conn.get_bucket(bucketname)
	mybucket.delete_key(username+'/media/'+filename)

