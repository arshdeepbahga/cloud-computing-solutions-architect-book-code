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

#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
import os    
import time
import datetime
import exifread
import json
import boto3  
import MySQLdb

app = Flask(__name__, static_url_path="")

UPLOAD_FOLDER = os.path.join(app.root_path,'static','media')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BASE_URL="http://localhost:5000/media/"
AWS_ACCESS_KEY="<enter>"
AWS_SECRET_KEY="<enter>"
REGION="us-east-1"
BUCKET_NAME="<enter>"
DB_HOSTNAME="photogallerydb.abc.us-east-1.rds.amazonaws.com"
DB_USERNAME = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'photogallerydb'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def getExifData(path_name):
    f = open(path_name, 'rb')
    tags = exifread.process_file(f)
    ExifData={}
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 
                       'Filename', 'EXIF MakerNote'):
            key="%s"%(tag)
            val="%s"%(tags[tag])
            ExifData[key]=val
    return ExifData

def s3uploading(filename, filenameWithPath):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY)
                       
    bucket = BUCKET_NAME
    path_filename = "photos/" + filename
    print path_filename
    s3.upload_file(filenameWithPath, bucket, path_filename)  
    s3.put_object_acl(ACL='public-read', 
                Bucket=bucket, Key=path_filename)

    return "http://"+BUCKET_NAME+\
            ".s3-website-us-east-1.amazonaws.com/"+ path_filename 

@app.route('/', methods=['GET', 'POST'])
def home_page():
    conn = MySQLdb.connect (host = DB_HOSTNAME,
                        user = DB_USERNAME,
                        passwd = DB_PASSWORD,
                        db = DB_NAME, 
            port = 3306)
    cursor = conn.cursor ()
    cursor.execute("SELECT * FROM photogallerydb.photogallery2;")
    results = cursor.fetchall()
    
    items=[]
    for item in results:
        photo={}
        photo['PhotoID'] = item[0]
        photo['CreationTime'] = item[1]
        photo['Title'] = item[2]
        photo['Description'] = item[3]
        photo['Tags'] = item[4]
        photo['URL'] = item[5]
        items.append(photo)
    conn.close()        
    print items
    return render_template('index.html', photos=items)

@app.route('/add', methods=['GET', 'POST'])
def add_photo():
    if request.method == 'POST':    
        uploadedFileURL=''
        file = request.files['imagefile']
        title = request.form['title']
        tags = request.form['tags']
        description = request.form['description']

        print title,tags,description
        if file and allowed_file(file.filename):
            filename = file.filename
            filenameWithPath = os.path.join(UPLOAD_FOLDER, filename)
            print filenameWithPath
            file.save(filenameWithPath)            
            uploadedFileURL = s3uploading(filename, filenameWithPath);
            ExifData=getExifData(filenameWithPath)
            print ExifData
            ts=time.time()
            timestamp = datetime.datetime.\
                        fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            conn = MySQLdb.connect (host = DB_HOSTNAME,
                        user = DB_USERNAME,
                        passwd = DB_PASSWORD,
                        db = DB_NAME, 
            port = 3306)
            cursor = conn.cursor ()

            statement = "INSERT INTO photogallerydb.photogallery2 \
                        (CreationTime,Title,Description,Tags,URL,EXIF) \
                        VALUES ("+\
                        "'"+str(timestamp)+"', '"+\
                        title+"', '"+\
                        description+"', '"+\
                        tags+"', '"+\
                        uploadedFileURL+"', '"+\
                        json.dumps(ExifData)+"');"
            
            print statement
            result = cursor.execute(statement)
            conn.commit()
            conn.close()

        return redirect('/')
    else:
        return render_template('form.html')

@app.route('/<int:photoID>', methods=['GET'])
def view_photo(photoID):    
    conn = MySQLdb.connect (host = DB_HOSTNAME,
                        user = DB_USERNAME,
                        passwd = DB_PASSWORD,
                        db = DB_NAME, 
            port = 3306)
    cursor = conn.cursor ()

    cursor.execute("SELECT * FROM photogallerydb.photogallery2 \
                    WHERE PhotoID="+str(photoID)+";")

    results = cursor.fetchall()

    items=[]
    for item in results:
        photo={}
        photo['PhotoID'] = item[0]
        photo['CreationTime'] = item[1]
        photo['Title'] = item[2]
        photo['Description'] = item[3]
        photo['Tags'] = item[4]
        photo['URL'] = item[5]
        photo['ExifData']=json.loads(item[6])
        items.append(photo)
    conn.close()        
    tags=items[0]['Tags'].split(',')
    exifdata=items[0]['ExifData']
    
    return render_template('photodetail.html', photo=items[0], 
                            tags=tags, exifdata=exifdata)

@app.route('/search', methods=['GET'])
def search_page():
    query = request.args.get('query', None)    
    conn = MySQLdb.connect (host = DB_HOSTNAME,
                        user = DB_USERNAME,
                        passwd = DB_PASSWORD,
                        db = DB_NAME, 
            port = 3306)
    cursor = conn.cursor ()
    
    cursor.execute("SELECT * FROM photogallerydb.photogallery2 \
                    WHERE Title LIKE '%"+query+ "%' \
                    UNION SELECT * FROM \
                    photogallerydb.photogallery2 WHERE \
                    Description LIKE '%"+query+ "%' UNION \
                    SELECT * FROM photogallerydb.photogallery2 \
                    WHERE Tags LIKE '%"+query+"%' ;")

    results = cursor.fetchall()

    items=[]
    for item in results:
        photo={}
        photo['PhotoID'] = item[0]
        photo['CreationTime'] = item[1]
        photo['Title'] = item[2]
        photo['Description'] = item[3]
        photo['Tags'] = item[4]
        photo['URL'] = item[5]
        photo['ExifData']=item[6]
        items.append(photo)
    conn.close()        
    print items
    return render_template('search.html', photos=items, 
                            searchquery=query)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
