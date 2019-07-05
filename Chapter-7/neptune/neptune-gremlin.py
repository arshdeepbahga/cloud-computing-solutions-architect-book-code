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

from __future__  import print_function  
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import \
				DriverRemoteConnection
from gremlin_python.process.traversal import Order
from gremlin_python.process.traversal import P
statics.load_statics(globals())

graph = Graph()

g = graph.traversal().withRemote(DriverRemoteConnection(
	'ws://mydb.cluster.us-east-1.neptune.amazonaws.com:8182/gremlin','g'))

#Add a vertex for a customer
c1 = g.addV('CUSTOMER').property('name', 'Bradley Russo').\
	property('address', '486, 6221 Et St.,Barnstaple').\
	property('country', 'Ukraine').\
	property('zipcode', '10903').next()

#Add a vertex for a customer
c2 = g.addV('CUSTOMER').property('name', 'Jarrod Nieves').\
	property('address', '198-550 At, Rd.,Hines Creek').\
	property('country', 'Greece').\
	property('zipcode', '20587').next()

#Add a vertex for a customer
c3 = g.addV('CUSTOMER').property('name', 'Ivor Merritt').\
	property('address', '527-9960 Vel Street,Lauw').\
	property('country', 'Peru').\
	property('zipcode', '5624').next()

#Add a vertex for a product
p1 = g.addV('PRODUCT').property('title', \
	'Motorola Moto G (3rd Generation)').\
	property('features', "Advanced water resistance,\
	13 MP camera, 5in HD display, \
	Quad core processing power, 5MP rear camera, \
	4G LTE Speed").\
	property('Color', 'Black').\
	property('Size', '16GB').\
	property('Dimensions', '0.2 x 2.9 x 5.6 inches').\
	property('Weight', '5.4 ounces').\
	property('price', 219.99).next()

#Add a vertex for a product
p2 = g.addV('PRODUCT').property('title', \
	'Canon EOS Rebel T5').property('features', \
	"18 megapixel CMOS (APS-C) sensor, \
	EF-S 18-55mm IS II standard zoom lens, \
	3-inch LCD TFT color,liquid-crystal monitor, \
	EOS 1080p full HD movie mode").\
	property('Color', 'Black').\
	property('MaximumAperture', 'f3.5').\
	property('Dimensions', '3.94 x 3.07 x 5.12 inches').\
	property('Weight', '1.06 pounds').\
	property('price', 399).next()

#Add edges for customers ordering products
r1 =  g.V(c1).addE('ORDERS').to(p1).\
	property('date',"2015-11-03").\
	property('quantity',2).next()

r2 =  g.V(c2).addE('ORDERS').to(p1).\
	property('date',"2015-11-03").\
	property('quantity',1).next()

r3 =  g.V(c1).addE('ORDERS').to(p2).\
	property('date',"2015-11-03").\
	property('quantity',1).next()

r4 =  g.V(c2).addE('ORDERS').to(p2).\
	property('date',"2015-11-03").\
	property('quantity',1).next()

#Add edges for customers rating products
r5 =  g.V(c1).addE('RATES').to(p1).\
	property('rating',4.8).next()

r6 =  g.V(c2).addE('RATES').to(p2).\
	property('rating',4.5).next()

#Print list of all vertices
print(g.V().toList())

#Print list of all customers
print(g.V().hasLabel('CUSTOMER').toList())
print(g.V().hasLabel('CUSTOMER').name.toList())

#Print list of all products
print(g.V().hasLabel('PRODUCT').toList())
print(g.V().hasLabel('PRODUCT').title.toList())

#Print list of all customers from the country Greece
print(g.V().hasLabel('CUSTOMER').\
	has('country','Greece').toList())

#Print list of all products with price greater than 100
print(g.V().hasLabel('PRODUCT').\
	has('price',P.gt(100)).\
	order().by('price',Order.decr).toList())
