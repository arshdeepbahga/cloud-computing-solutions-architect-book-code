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

from random import randint 
import time 
import datetime 
import requests 
import json 
 
def getData(): 
    ts=time.time() 
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 
    temp = str(randint(0,100)) 
    humidity = str(randint(0,100)) 
    co2 = str(randint(50,500)) 
    light = str(randint(0,10000)) 
    data = {"timestamp": timestamp, "temperature": temp, 
    "humidity": humidity , "co2": co2, "light": light} 
    return data 
 
def publish(datadir): 
    r = requests.post("http://localhost:5000/api/data", 
    data = json.dumps(datadir), 
    headers={"Content-Type": "application/json"}) 
     
while True: 
    data = getData() 
    print data 
    publish(data) 
    time.sleep(1)
