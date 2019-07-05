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
import sys 
 
#Calculates mean temperature, humidity, light and CO2  
# Input data format: 
#"2014-04-29 10:15:32",37,44,31,6 
#Output:  
#"2014-04-29 10:15    [48.75, 31.25, 29.0, 16.5]" 
 
#Input comes from STDIN (standard input) 
for line in sys.stdin: 
    # remove leading and trailing whitespace 
    line = line.strip() 
    data = line.split(',') 
    l=len(data) 
 
    #For aggregation by minute  
    key=str(data[0][0:17]) 
 
    value=data[1]+','+data[2]+','+data[3]+','+data[4] 
    print '%s\t%s' % (key, value)
