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

#!/usr/bin/env python

from httperfpy import Httperf

#Run in 5 steps and increment request rate by 10 in each step
for i in range(10,60,10):
    print 'Rate='+str(i)
    perf =  Httperf(server="www.mywebsite.com", 
            port=80,rate=i,num_calls=50,
            num_conns=400,timeout=60, 
            send_buffer=4096,recv_buffer=16384)

    perf.parser = True

    results = perf.run()

    print 'Request rate per sec, Connection rate per sec, Avg reply rate, Max reply rate, Response Time'
    print results["request_rate_per_sec"] + ', '+ results["connection_rate_per_sec"] +  ', '+ results["reply_rate_avg"] +  ','+ results["reply_rate_max"]+', '+results["reply_time_response"]


