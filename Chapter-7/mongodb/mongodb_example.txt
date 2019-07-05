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


#Launch MongoDB shell 
mongo localhost:27017 
 
#Switch to new database named storedb 
> use storedb 
switched to db storedb 
 
post = { 
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
 
> db.collection.insert(post) 
WriteResult({ "Inserted" : 1 }) 
 
#Get all documents
> db.collection.find() 
{ "_id" : ObjectId("56fd4f59849f6367af489537"),  
"title" : "Motorola Moto G (3rd Generation)",  
"features" : [ "Advanced water resistance",  
"13 MP camera which includes a color-balancing dual LED Flash",  
"5in HD display", "Quad core processing power", "5MP rear camera", 
"Great 24hr battery performance with a 2470mAh battery", "4G LTE Speed" ], 
"specifications" : { "Color" : "Black", "Size" : "16 GB",  
"Dimensions" : "0.2 x 2.9 x 5.6 inches", "Weight" : "5.4 ounces" }, "price" : 219.99 } 
 
{ "_id" : ObjectId("56fd504d849f6367af489538"),  
"title" : "Canon EOS Rebel T5",  
"features" : [ "18 megapixel CMOS (APS-C) sensor", 
 "EF-S 18-55mm IS II standard zoom lens",  
 "3-inch LCD TFT color, liquid-crystal monitor", 
  "EOS 1080p full HD movie mode" ],  
  "specifications" : { "Color" : "Black",  
  "MaximumAperture" : "f3.5", "Dimensions" : "3.94 x 3.07 x 5.12 inches",  
  "Weight" : "1.06 pounds" }, "price" : 399 } 
 
#Get documents with specific attribute values
> db.collection.find({"title" : "Canon EOS Rebel T5"}) 
{ "_id" : ObjectId("56fd504d849f6367af489538"),  
"title" : "Canon EOS Rebel T5",  
"features" : [ "18 megapixel CMOS (APS-C) sensor",  
"EF-S 18-55mm IS II standard zoom lens", 
 "3-inch LCD TFT color, liquid-crystal monitor",  
 "EOS 1080p full HD movie mode" ],  
 "specifications" : { "Color" : "Black",  
 "MaximumAperture" : "f3.5", "Dimensions" : "3.94 x 3.07 x 5.12 inches",  
 "Weight" : "1.06 pounds" }, "price" : 399 }
 
