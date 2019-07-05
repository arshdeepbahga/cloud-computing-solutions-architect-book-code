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

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from boto.sqs.message import Message
import cPickle


consumer_key="<enter>"
consumer_secret="<enter>"
access_token = "<enter>"
access_token_secret = "<enter>"


import boto.sqs
conn = boto.sqs.connect_to_region(
     "us-east-1",
     aws_access_key_id='<enter>',
     aws_secret_access_key='<enter>')

q = conn.get_all_queues(prefix='arsh-queue')

class StdOutListener(StreamListener):
	def on_data(self, data):
		#print data
		msg=cPickle.dumps(data)
		m = Message()
		m.set_body(msg)
		status = q[0].write(m)
		return True

   	def on_error(self, status):
        	print status


if __name__ == '__main__':
	keywords=['india']
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	stream = Stream(auth, l)
	stream.filter(track=keywords)


