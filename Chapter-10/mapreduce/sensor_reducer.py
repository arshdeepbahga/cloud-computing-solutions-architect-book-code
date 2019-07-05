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
from operator import itemgetter 
import sys 
import numpy as np 
 
current_key = None 
current_vals_list = [] 
word = None 
 
#Input comes from STDIN 
for line in sys.stdin: 
    # remove leading and trailing whitespace 
    line = line.strip() 
 
#Parse the input from mapper 
    key, values = line.split('\t', 1) 
    list_of_values = values.split(',') 
     
#Convert to list of strings to list of int
    list_of_values = [int(i) for i in list_of_values] 
    
    if current_key == key: 
        current_vals_list.append(list_of_values) 
    else: 
        if current_key: 
            l = len(current_vals_list)+ 1 
            b =np.array(current_vals_list) 
            meanval =[np.mean(b[0:l,0]),np.mean(b[0:l,1]), np.mean(b[0:l,2]), np.mean(b[0:l,3])]
            print '%s\t%s' % (current_key,str(meanval)) 
 
        current_vals_list = [] 
        current_vals_list.append(list_of_values) 
        current_key = key 
 
#Output the last key if needed 
if current_key == key:
    l = len(current_vals_list)+ 1 
    b = np.array(current_vals_list) 
    meanval = [np.mean(b[0:l,0]),np.mean(b[0:l,1]),np.mean(b[0:l,2]), np.mean(b[0:l,3])] 
    print '%s\t%s' % (current_key, str(meanval))
