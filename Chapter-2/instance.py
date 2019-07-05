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

@app.route('/')
def hello_world():
    BASEURL='http://169.254.169.254/latest/meta-data/'
	response = urllib2.urlopen(BASEURL+'hostname')
	hostname = response.read()
	response = urllib2.urlopen(BASEURL+'instance-id')
	instanceid = response.read()
	response = urllib2.urlopen(BASEURL+'public-ipv4')
	publicipv4 = response.read()

	html = 'Hostname: '+hostname+'<br>'+'Instance-ID: '+\
            instanceid+'<br>'+'Public-IP: '+publicipv4
	return html

if __name__ == '__main__':
    app.run(host='0.0.0.0')
