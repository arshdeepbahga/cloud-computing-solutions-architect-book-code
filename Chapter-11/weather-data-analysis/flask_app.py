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
app = Flask(__name__) 
import blist 
 
from cassandra.cluster import Cluster 
 
cluster = Cluster(['127.0.0.1']) 
session = cluster.connect('predictions') 
 
@app.route('/') 
def tweet_home(): 
 
 
    html = '<html><body><table width=80% border=1 align="center">'+'<tr><td><strong>Timestamp</strong></td>'+'<td><strong>Fog Prediction</strong></td>'+'<td><strong>Haze Prediction</strong></td></tr>' 
 
    data = session.execute('SELECT * FROM data') 
    for each in data: 
        html+='<td>'+each.timestamp+'</td><td>'+ each.fog_prediction+'</td><td>'+ each.haze_prediction+'</td></tr>' 
 
    html+='</table></body></html>' 
 
    return html 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0') 
