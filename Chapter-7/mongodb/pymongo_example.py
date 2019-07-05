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

import time 
from datetime import date 
import datetime 
import cPickle 
from pymongo import MongoClient 
 
client = MongoClient() 
db = client['storedb'] 
collection = db['current'] 
 
item = { 
    "title" : "Motorola Moto G (3rd Generation)", 
    "features" : [ 
        "Advanced water resistance", 
        "13 MP camera which includes a color-balancing dual LED Flash", 
        "5in HD display", 
        "Quad core processing power", 
        "5MP rear camera", 
        "Great 24hr battery performance with a 2470mAh battery", 
        "4G LTE Speed" 
    ], 
    "specifications" : { 
        "Color" : "Black", 
        "Size" : "16 GB", 
        "Dimensions" : "0.2 x 2.9 x 5.6 inches", 
        "Weight" : "5.4 ounces" 
    }, 
    "price" : 219.99 
} 
 
#Insert an item 
collection.insert_one(item) 
 
#Retrieve all items 
results=db.collection.find() 
for item in results: 
    print item 
     
#Find an item 
results = collection.find({"title" : "Motorola Moto G"}) 
 
for item in results: 
    print item 
