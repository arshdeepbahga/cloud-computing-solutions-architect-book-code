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

from pymongo import MongoClient
import datetime
import boto.sqs
from boto.sqs.message import Message
import cPickle
from datetime import date
import json
from topia.termextract import extract
from collections import OrderedDict
import re
import ast
import random
import sys

parseddic={}
aggregatedic={}
TERMS={}
global conn
global q
global client 
global db
global keyword
###########################################################################
#Setup Consumer function: requires list_of_cities.txt, AFINN-111.txt, 
#                geocoded_locations.txt, keywords.txt, topissues.txt
############################################################################
def setupConsumer():
	global conn
	global q
	global client 
	global db
	global keyword

	#------Initialize keyword list---------
	keyword='india'
	
	#-----Load Sentiments Dict----------------
	sent_file = open('AFINN-111.txt')
	sent_lines = sent_file.readlines()
	for line in sent_lines:
		s = line.split("\t")
		TERMS[s[0]] = s[1]

	sent_file.close()

	
	#-------Connect to SQS Queue----------------
	conn = boto.sqs.connect_to_region(
		"us-east-1",
		aws_access_key_id='<enter>',
		aws_secret_access_key='<enter>')

	q = conn.get_queue('arsh-queue')
	queuecount=q.count()
	print "Queue count= "+str(queuecount)

	#-------Connect to MongoDB----------------
	client = MongoClient()
	client = MongoClient('localhost', 27017)
	db = client['myapp']

   

############### Find Sentiment function ################
def findsentiment(tweet):
	splitTweet=tweet.split()
	sentiment=0.0
	for word in splitTweet:
		if TERMS.has_key(word):
			sentiment = sentiment+ float(TERMS[word])
	return sentiment

############### Parse Tweet function #######################
def parseTweet(tweet):
	if tweet.has_key('created_at'):
		createdat = tweet['created_at']
		hourint=int(createdat[11:13])
		parseddic['hour'] = str(hourint)

#-------------------Reteets---------------------------------------------
	parseddic['toptweets']={}
	if tweet.has_key('retweeted_status'):
		retweetcount=tweet['retweeted_status']['retweet_count']
		retweetscreenname=tweet['retweeted_status']['user']['screen_name'].encode('utf-8',errors='ignore')
		retweetname=tweet['retweeted_status']['user']['name'].encode('utf-8',errors='ignore')
		retweetuserpic=tweet['retweeted_status']['user']['profile_image_url']
		retweettext=tweet['retweeted_status']['text'].encode('utf-8',errors='ignore')
		retweetdic={}
		retweetdic['retweetcount']=retweetcount
		retweetdic['retweetscreenname']=retweetscreenname
		retweetdic['retweetname']=retweetname
		retweetdic['retweettext']=retweettext
		retweetdic['retweetimage']=retweetuserpic
		retweetdic['retweetsentiment']=findsentiment(retweettext)
		parseddic['toptweets']=retweetdic


#-------------------Text, Sentiment, Keywords---------------------------------------------
	if tweet.has_key('text'):
		text = tweet['text'].encode('utf-8',errors='ignore')
		parseddic['text']=text
		sentiment=findsentiment(text)
		parseddic['sentimentscore']=sentiment
		parseddic['positivesentiment']=0
		parseddic['negativesentiment']=0
		parseddic['neutralsentiment']=0

		if sentiment>0:
			parseddic['positivesentiment']=1
		elif sentiment<0:
			parseddic['negativesentiment']=1
		elif sentiment==0:
			parseddic['neutralsentiment']=1


#-------------------Hashtags---------------------------------------------
	if tweet.has_key('entities'):
		res1 = tweet['entities']	
		taglist = res1["hashtags"]
		hashtaglist=[]
		for tagitem in taglist:
			hashtaglist.append(tagitem["text"])
		parseddic['hashtags']=hashtaglist


############### Analyze Tweet function ################
def analyzeTweet(tweetdic):
	text =tweetdic['text']
	text =text.lower()
		
	if not aggregatedic.has_key(keyword):
		valuedic={'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0,  'hashtags': {}, 'toptweets': {}, 'totalretweets':0, 'hourlyaggregate':{'0': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'1': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'2': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'3': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'4': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'5': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'6': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'7': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'8': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'9': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'10': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'11': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'12': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'13': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'14': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'15': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'16': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'17': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'18': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'19': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'20': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0}, '21': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0}, '22': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0},'23': {'totaltweets':0, 'positivesentiment':0,'negativesentiment':0,'neutralsentiment': 0}} }
		aggregatedic[keyword]=valuedic

#-------------------Counts---------------------------------------------
	valuedic=aggregatedic[keyword]
	valuedic['totaltweets']+=1
	valuedic['positivesentiment']+=tweetdic['positivesentiment']
	valuedic['negativesentiment']+=tweetdic['negativesentiment']
	valuedic['neutralsentiment']+=tweetdic['neutralsentiment']

#-------------------Hourly Aggregate---------------------------------------------
	hour=tweetdic['hour']
	valuedic['hourlyaggregate'][hour]['positivesentiment']+=tweetdic['positivesentiment']
	valuedic['hourlyaggregate'][hour]['negativesentiment']+=tweetdic['negativesentiment']
	valuedic['hourlyaggregate'][hour]['neutralsentiment']+=tweetdic['neutralsentiment']
	valuedic['hourlyaggregate'][hour]['totaltweets']+=1

#-------------------Top Hashtags---------------------------------------------
	tagsdic=valuedic['hashtags'] 
	for tag in tweetdic['hashtags']:
		if tagsdic.has_key(tag):
			tagsdic[tag]+=1
		else:
			tagsdic[tag]=1


#-------------------Top Tweets---------------------------------------------
	if tweetdic.has_key('toptweets'): 
		if tweetdic['toptweets'].has_key('retweetscreenname'):
			toptweetsdic=valuedic['toptweets']
			retweetkey= tweetdic['toptweets']['retweetscreenname']

			if toptweetsdic.has_key(retweetkey):
				toptweetsdic[retweetkey]['retweetcount']=tweetdic['toptweets']['retweetcount']
			else:
				toptweetsdic[retweetkey]=tweetdic['toptweets']
	

#-------------------Aggregate---------------------------------------------
	aggregatedic[keyword]=valuedic 
		

############### Post Processing function #####################
def postProcessing():
	print aggregatedic
	valuedic= aggregatedic[keyword]


#-------------------------Top 10 Hashtags------------------
	keysdic=valuedic['hashtags'] 
	sortedkeysdic = OrderedDict(sorted(keysdic.items(),key = lambda x:x[1],reverse=True))
	tophashtagsdic={}
	i=0
	for item in sortedkeysdic:
		if i>9:
			break
		i = i+1
		tophashtagsdic[item]= keysdic[item]

	valuedic['hashtags']=tophashtagsdic


#---------------------Total Retweets & Top 10 Tweets----------------------
	toptweetsdic=valuedic['toptweets'] 
	for key in toptweetsdic:
		valuedic['totalretweets']+=toptweetsdic[key]['retweetcount']

	sortednames=sorted(toptweetsdic,key = lambda x:toptweetsdic[x]['retweetcount'],reverse=True)
	sortedtoptweetsdic = OrderedDict()
	i=0
	for k in sortednames:
		if i>99:
			break
		i = i+1
		sortedtoptweetsdic[k]=toptweetsdic[k]	

	valuedic['toptweets'] = sortedtoptweetsdic
	#print valuedic['toptweets']



#-----------------Create Key for MongoDB document---------------------------
	valuedic['_id'] = str(date.today())+"/"+keyword
	valuedic['metadata'] = {'date': str(date.today()), 'key': keyword}

	
#------------------Insert into MongoDB--------------------------------------
	print valuedic
	print "Inserting data into MongoDB"
	postid=db.myapp_micollection.insert(valuedic)



################### Main Function: Configure consumeCount ###############
def main():
	print "Setting up consumer..."
	setupConsumer()
	print "Completed consumer setup..."

	#------enter no. of tweets to consume------------
	consumeCount=800

	print "Consuming "+ str(consumeCount) +" feeds..."

	consumeCount=consumeCount/10 #get 10 in each batch
	for i in range(consumeCount):
		rs = q.get_messages(10) #gets max 10 msgs at a time.
		if len(rs) > 0:
		    for m in rs:
			post=m.get_body()
			deserializedpost=cPickle.loads(post)
			postdic=json.loads(deserializedpost)
		
			parseTweet(postdic)
			analyzeTweet(parseddic)
		conn.delete_message_batch(q,rs)
	
	queuecount=q.count()
	print "Remaining Queue count= "+str(queuecount)	

	print "Completed consuming..."
	print "Starting post processing..."
	postProcessing()
	print "Completed post processing..."
	print "Done!"

###########Entry Point####################
if __name__ == '__main__':
    main()





