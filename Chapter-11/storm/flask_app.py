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

from flask import Flask 
import urllib2 
import boto.dynamodb2 
from boto.dynamodb2.table import Table 
app = Flask(__name__) 
from datetime import date 
today = date.today() 
 
#-------Connect to DynamoDB--------- 
ACCESS_KEY="<Enter>" 
SECRET_KEY="<Enter>" 
REGION="us-east-1" 
 
conn_db = boto.dynamodb.connect_to_region(REGION, 
   aws_access_key_id=ACCESS_KEY, 
   aws_secret_access_key=SECRET_KEY) 
 
table = conn_db.get_table('twittersentiment') 
#----------------------------------- 
    
@app.route('/') 
def tweet_home(): 
 
    #Scan DynamoDB table 
    results=table.scan() 
     
    html = '<html><body><table width=80% border=1 align="center">'+'<tr><td><strong>Timestamp</strong></td>'+'<td><strong>Date</strong></td>' +'<td><strong>Tweet</strong></td> '+'<td><strong>Sentiment</strong></td> '+'</tr>' 
             
    for result in results: 
        html+='<tr><td>'+result['timestamp']+'</td><td>'+ result['date']+'</td><td>'+result['tweet']+'</td><td>'+ result['sentiment']+'</td></tr>' 
 
    html+='</table></body></html>' 
 
    return html 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0')
