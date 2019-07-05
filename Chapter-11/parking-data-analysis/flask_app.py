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

from flask import Flask, render_template  
from cassandra.cluster import Cluster 
 
cluster = Cluster() 
app = Flask(__name__) 
 
@app.route('/') 
def index(): 
    session = cluster.connect('test') 
    lot1 = session.execute('Select occrate, price from smartpark where lotid = 1 limit 1') 
    lot2 = session.execute('Select occrate, price from smartpark where lotid = 2 limit 1') 
    lot3 = session.execute('Select occrate, price from smartpark where lotid = 3 limit 1') 
    return render_template('index.html', price1=str(lot1[0].price),  
        price2=str(lot2[0].price), price3=str(lot3[0].price),  
        occrate1=str(lot1[0].occrate), occrate2=str(lot2[0].occrate),  
        occrate3=str(lot3[0].occrate)) 
 
@app.route('/ParkingLot/<pid>') 
def ParkingLot(pid=1): 
    session = cluster.connect('test') 
    lot = session.execute('Select occrate,price from smartpark where lotid = %s limit 30', [int(pid)]) 
    return render_template('plot.html', pid=pid, price=lot[0].price, occrate= lot[0].occrate, lot=lot) 
 
if __name__ == '__main__':  
    app.run(host='0.0.0.0', debug = True)
