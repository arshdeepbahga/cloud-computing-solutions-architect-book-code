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

#Sample output -
#{'ST102': {0: 265.79999999999995, 1: 316.935922330097, 
#        2: 0.49251456310679603, 3: 2.318446601941748}, 
#'ST105': {0: 266.98867924528304, 1: 307.3669811320756, 
#       2: 0.46788679245283016, 3: 2.5303773584905658}}

#!/usr/bin/env python
from operator import itemgetter
import sys
import ast

stationIDs=[]
value=0
total_value={}
count={}
avg_value = {}

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # parse the input we got from mapper
    stationID, valuesStr = line.split('\t', 1)
    stationIDs.append(stationID)

    try:
        values = ast.literal_eval(str(valuesStr))
        if type(values) == tuple:
            pass
        else:
            continue            
    except:
        continue

    if total_value.has_key(stationID):
        i=0
        for value in values:            
            total_value[stationID][i]=total_value[stationID][i]+value        
            i=i+1
        count[stationID]=count[stationID]+1
    else:
        i=0
        total_value[stationID]={}
        avg_value[stationID]={}
        for value in values:
            total_value[stationID][i]=value        
            i=i+1
        count[stationID]=1

for stationID in stationIDs:
    for i in range(0,4):
        avg_value[stationID][i]=total_value[stationID][i]/count[stationID]

print avg_value
