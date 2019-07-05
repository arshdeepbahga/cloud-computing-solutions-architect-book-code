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


# Start thrift server first: 
# hbase thrift start

import happybase

connection = happybase.Connection(host='localhost')
table = connection.table('products')

# Put    
table.put('row-1', {'details:name': 'Cloud Book'})

# Get 
row = table.row('row-1')
print row['details:name']  

# Scan
for key, data in table.scan():
    print key, data
    
# Delete row 
row = table.delete('row-1')

# Batch put    
b = table.batch()
b.put('row-key-1', {'details:name': 'Cloud Book', 
'details:ISBN': '9781494435141', 
'sale:StartSale': '01-01-2014', 'sale:Price':'50'}) 

b.put('row-key-2', {'details:name': 'IoT Book', 
'details:ISBN': '9780996025515', 
'sale:StartSale': '01-01-2015', 'sale:Price':'55'})
b.send()

