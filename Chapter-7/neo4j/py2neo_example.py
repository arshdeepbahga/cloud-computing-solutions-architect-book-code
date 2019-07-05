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

import py2neo 
from py2neo import Graph, Node, Relationship 
 
# Authenticate the user using py2neo.authentication 
py2neo.authenticate("localhost:7474", "neo4j", "password") 
 
# Connect to Graph and get the instance of Graph 
graph = Graph("http://localhost:7474/db/data/") 
 
#Define nodes 
c1 = Node("CUSTOMER", name="Bradley Russo", 
    address="486, 6221 Et St.,Barnstaple", 
    country="Ukraine", zipcode="10903") 
     
c2 = Node("CUSTOMER", name="Jarrod Nieves", 
    address="198-550 At, Rd.,Hines Creek", 
    country="Greece", zipcode="10903") 
     
c3 = Node("CUSTOMER", name="Ivor Merritt", 
    address="527-9960 Vel Street,Lauw", 
    country="Peru", zipcode="5624") 
 
p1 = Node("PRODUCT",title = "Motorola Moto G (3rd Generation)",  
    features = ["Advanced water resistance", "13 MP camera",  
    "5in HD display", "Quad core processing power",  
    "5MP rear camera", "4G LTE Speed"],  
    Color ="Black", Size = "16GB",  
    Dimensions = "0.2 x 2.9 x 5.6 inches", 
     Weight = "5.4 ounces",price =  219.99) 
 
p2=Node("PRODUCT",title = "Canon EOS Rebel T5",  
    features = ["18 megapixel CMOS (APS-C) sensor",  
    "EF-S 18-55mm IS II standard zoom lens", "3-inch LCD TFT color",  
    "liquid-crystal monitor", "EOS 1080p full HD movie mode",  
    Color = "Black", MaximumAperture = "f3.5",  
    Dimensions = "3.94 x 3.07 x 5.12 inches",  
    Weight = "1.06 pounds", price = 399) 
 
#Define relationships 
r1 = Relationship(c1,"ORDERS",p1,date="2015-11-03", quantity="2") 
r2 = Relationship(c2,"ORDERS",p1,date="2015-11-03", quantity="1") 
r3 = Relationship(c1,"ORDERS",p2,date="2015-11-03", quantity="1") 
r4 = Relationship(c2,"ORDERS",p2,date="2015-11-03", quantity="1") 
 
r5 = Relationship(c1,"RATES",p1,rating="4.8") 
r6 = Relationship(c2,"RATES",p2,quantity="4.5") 
 
#Create nodes 
result = graph.create(c1, c2, p1, p2) 
 
#Create relationships 
result = graph.create(r1, r2, r3, r4, r5, r6) 
 
#Print the results 
print result
