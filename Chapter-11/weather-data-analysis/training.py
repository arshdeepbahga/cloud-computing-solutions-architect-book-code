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

from sklearn import svm 
import csv 
import numpy as np 
from sklearn.externals import joblib 
 
def is_number(s): 
    try: 
        float(s) # for int, long and float 
    except ValueError: 
        return False 
 
    return True 
 
 
def svmTrain(): 
    f = open('PositiveHaze.csv') 
    csv_f = csv.reader(f) 
    tList=[] 
    tClass=[] 
    counter=0 
    for row in csv_f: 
        new_list=[] 
        if counter < 2: 
            counter=counter+1 
            continue 
        for item in row: 
            if not(is_number(item)): 
                continue 
            new_list.append(float(item)) 
        print new_list 
        if len(new_list)!=5: 
            print "ERROR" 
            continue 
        tList.append(new_list) 
        tClass.append(1) 
 
    f.close() 
     
    f=open('NegativeHazeAndNegativeFog.csv') 
    csv_f=csv.reader(f) 
    counter=0 
    for row in csv_f: 
        new_list=[] 
        if counter < 2: 
            counter=counter+1 
            continue 
        for item in row: 
            if not(is_number(item)): 
                continue 
            new_list.append(float(item)) 
        print new_list 
        if len(new_list)!=5: 
            print "ERROR" 
            continue 
        tList.append(new_list) 
        tClass.append(0) 
 
    f.close(); 
    f=open('PositiveFog.csv') 
    csv_f= csv.reader(f) 
    tFogList=[] 
    tFogClass=[] 
    counter=0 
 
    for row in csv_f: 
        new_list=[] 
        if counter < 2: 
            counter=counter+1 
            continue 
        for item in row: 
            if not(is_number(item)): 
                continue 
            new_list.append(float(item)) 
        print new_list 
        if len(new_list)!=5: 
            continue 
            exit(2) 
        tFogClass.append(1) 
        tFogList.append(new_list) 
 
    f.close() 
    f=open('NegativeHazeAndNegativeFog.csv') 
    csv_f=csv.reader(f) 
    counter=0 
    for row in csv_f: 
        new_list=[] 
        if counter < 2: 
            counter=counter+1 
            continue 
        for item in row: 
            if not(is_number(item)): 
                continue 
            new_list.append(float(item)) 
        print new_list 
        if len(new_list)!=5: 
            continue 
        tFogClass.append(0) 
        tFogList.append(new_list) 
 
    svmThunder = svm.SVC() 
 
    svmThunder.fit(tList,tClass) 
 
    svmFog = svm.SVC() 
 
    svmFog.fit(tFogList,tFogClass) 
 
    joblib.dump(svmThunder, 'svmHaze.pkl') 
    joblib.dump(svmFog, 'svmFog.pkl' ) 
 
 
if __name__ == '__main__': 
    svmTrain() 
