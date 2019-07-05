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

import MySQLdb

USERNAME = 'root'
PASSWORD = 'password'
DB_NAME = 'mytestdb'

print "Connecting to RDS instance"

conn = MySQLdb.connect (host = "<enter>",
                        user = USERNAME,
                        passwd = PASSWORD,
                        db = DB_NAME, 
			port = 3306)

print "Connected to RDS instance"

cursor = conn.cursor ()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone ()
print "server version:", row[0]

cursor.execute ("CREATE TABLE \
    Student(Id INT PRIMARY KEY, Name TEXT, Major TEXT, Grade FLOAT) ")
cursor.execute ("INSERT INTO Student VALUES(100, 'John', 'CS', 3)")
cursor.execute ("INSERT INTO Student VALUES(101, 'David', 'ECE', 3.5)")
cursor.execute ("INSERT INTO Student VALUES(102, 'Bob', 'CS', 3.9)")
cursor.execute ("INSERT INTO Student VALUES(103, 'Alex', 'CS', 3.6)")
cursor.execute ("INSERT INTO Student VALUES(104, 'Martin', 'ECE', 3.1)")

cursor.execute("SELECT * FROM Student")
rows = cursor.fetchall()

for row in rows:
	print row

cursor.close ()
conn.close ()
