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
DB_USERNAME = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'photogallerydb'

conn = MySQLdb.connect(host = "dbendpoint.us-east-1.rds.amazonaws.com",
                        user = DB_USERNAME,
                        passwd = DB_PASSWORD,
                        db = DB_NAME, 
                        port = 3306)

cursor = conn.cursor ()
cursor.execute ("SELECT VERSION()")

cursor.execute ("CREATE TABLE photogallery2 ( \
    PhotoID int PRIMARY KEY NOT NULL AUTO_INCREMENT, \
    CreationTime TEXT NOT NULL, \
    Title TEXT NOT NULL, \
    Description TEXT NOT NULL, \
    Tags TEXT NOT NULL, \
    URL TEXT NOT NULL,\
    EXIF TEXT NOT NULL\
    );")

cursor.close ()
conn.close ()