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
from flask import Flask, session, jsonify, abort, request, make_response
from flask import render_template, redirect
import os  
import time
import datetime
import exifread
import json
import boto3  
import MySQLdb
from botocore.exceptions import ClientError

application = Flask(__name__, static_url_path="")
application.secret_key = 'super secret key'

UPLOAD_FOLDER = os.path.join(application.root_path,'static','media')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BASE_URL="http://localhost:5000/media/"
REGION="us-east-1"
BUCKET_NAME="<enter-s3-bucket-name>"
DB_HOSTNAME="<enter-rds-instance-endpoint>"
DB_USERNAME = 'root'
DB_PASSWORD = 'gallery123'
DB_NAME = 'photogallerydb'
USER_POOL_ID="<enter-cognito-pool-id>"
CLIENT_ID="<enter-cognito-app-client-id>"
cognitoclient = boto3.client('cognito-idp', region_name=REGION)

@application.route('/healthcheck', methods=['GET'])
def healthcheck():
  result = {'response': 'true'}
  return make_response(jsonify(result), 201)
  
def allowed_file(filename):
  return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.errorhandler(400)
def bad_request(error):
  return make_response(jsonify({'error': 'Bad request'}), 400)

@application.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

def getExifData(path_name):
  f = open(path_name, 'rb')
  tags = exifread.process_file(f)
  ExifData={}
  for tag in tags.keys():
    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 
            'Filename', 'EXIF MakerNote'):
      #print "Key: %s, value %s" % (tag, tags[tag])
      key="%s"%(tag)
      val="%s"%(tags[tag])
      ExifData[key]=val
  return ExifData

def s3uploading(filename, filenameWithPath):
  s3 = boto3.client('s3')
             
  bucket = BUCKET_NAME
  path_filename = "photos/" + filename
  print path_filename
  s3.upload_file(filenameWithPath, bucket, path_filename)  
  s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=path_filename)
  return "http://"+BUCKET_NAME+".s3-website-us-east-1.amazonaws.com/"+ 
      path_filename 

@application.route('/', methods=['GET', 'POST'])
def home_page():
  if 'username' in session:
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
    userdata=session['name']+' ('+session['email']+')'
    return render_template('index.html', photos=items, userdata=userdata)
  else:
    return redirect('/login')

@application.route('/add', methods=['GET', 'POST'])
def add_photo():
  if 'username' in session:
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
        timestamp = datetime.datetime.fromtimestamp(ts).\
                    strftime('%Y-%m-%d %H:%M:%S')

        conn = MySQLdb.connect (host = DB_HOSTNAME,
              user = DB_USERNAME,
              passwd = DB_PASSWORD,
              db = DB_NAME, 
        port = 3306)
        cursor = conn.cursor ()
        statement = "INSERT INTO photogallerydb.photogallery2 \
              (CreationTime,Title,Description,Tags,URL,EXIF) VALUES ("+\
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
          userdata=session['name']+' ('+session['email']+')'
          return render_template('form.html', userdata=userdata)
  else:
    return redirect('/login')


@application.route('/<int:photoID>', methods=['GET'])
def view_photo(photoID):  
  if 'username' in session:
    conn = MySQLdb.connect (host = DB_HOSTNAME,
              user = DB_USERNAME,
              passwd = DB_PASSWORD,
              db = DB_NAME, 
        port = 3306)
    cursor = conn.cursor ()
    cursor.execute("SELECT * FROM photogallerydb.photogallery2 WHERE\
           PhotoID="+str(photoID)+";")
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
    userdata=session['name']+' ('+session['email']+')'
    return render_template('photodetail.html', photo=items[0], tags=tags, 
              exifdata=exifdata, userdata=userdata)
  else:
    return redirect('/login')

@application.route('/search', methods=['GET'])
def search_page():
  if 'username' in session:
    query = request.args.get('query', None)  
    conn = MySQLdb.connect (host = DB_HOSTNAME,
              user = DB_USERNAME,
              passwd = DB_PASSWORD,
              db = DB_NAME, 
        port = 3306)
    cursor = conn.cursor ()
    cursor.execute("SELECT * FROM photogallerydb.photogallery2 WHERE \
            Title LIKE '%"+query+ "%' UNION \
            SELECT * FROM photogallerydb.photogallery2 WHERE \
            Description LIKE '%"+query+ "%' UNION \
            SELECT * FROM photogallerydb.photogallery2 WHERE \
            Tags LIKE '%"+query+"%' ;")
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
    userdata=session['name']+' ('+session['email']+')'
    return render_template('search.html', photos=items, 
          searchquery=query, userdata=userdata)
  else:
    return redirect('/login')

def login_user(username,password):
  result=False
  message=""
  response={}
  try:
    response = cognitoclient.admin_initiate_auth(
      UserPoolId=USER_POOL_ID,
      ClientId=CLIENT_ID,
      AuthFlow='ADMIN_NO_SRP_AUTH',
      AuthParameters={
        'USERNAME': username,
        'PASSWORD': password
      }
    )
  except ClientError as e:
    if e.response['Error']['Code'] == 'UserNotFoundException':
      result=False
      message=="Can't Find user by Email"
    if e.response['Error']['Code'] == 'NotAuthorizedException':
      result=False
      message="Incorrect username or password"
    if e.response['Error']['Code'] == 'UserNotConfirmedException':
      result=False
      message="User is not confirmed"
    print e

  if 'ResponseMetadata' in response:
    if response['ResponseMetadata']['HTTPStatusCode']==200:    
      session['username'] = username
      get_user_data()
      result=True
      message="Login successful"
    else:
      return False
      message="Something went wrong"
  return result,message

def get_user_data():
  response = cognitoclient.admin_get_user(
    UserPoolId=USER_POOL_ID,
    Username=session['username']
  )
  for item in response['UserAttributes']:
    if item['Name']=='name':
      session['name']=item['Value']
    elif item['Name']=='email':
      session['email']=item['Value']
    elif item['Name']=='email_verified':
      session['email_verified']=item['Value']      

@application.route('/login', methods = ['GET', 'POST'])
def login():
  if request.method == 'POST':
    result,message=login_user(request.form['username'],
                    request.form['password']) 
    if result:     
      return redirect('/')
    else:
      return render_template('login.html', message=message)
  return render_template('login.html', message='')

@application.route('/logout')
def logout():
  # remove the username from the session if it is there
  session.pop('username', None)
  return redirect('/')

def signup_user(username, password, password1, name, email):
  print username, password, password1, name, email
  result=False
  message=""
  if password!=password1:
    result=False
    message="Passwords do not match"
    return result,message
  else:
    try:
      response = cognitoclient.sign_up(
        ClientId=CLIENT_ID,
        Username=username,
        Password=password,
        UserAttributes=[
          {
            'Name': 'name',
            'Value': name
          },
          {
            'Name': 'email',
            'Value': email
          }
        ]
      )
      result=True
      message="Signup successful"
    except ClientError as e:
      if e.response['Error']['Code'] == 'UsernameExistsException':
        result=False
        message="User already exists"
      if e.response['Error']['Code'] == 'ParamValidationError':
        result=False
        message="Param Validation Error"
    return result,message  

@application.route('/signup', methods = ['GET', 'POST'])
def signup():
  if request.method == 'POST':
    result,message=signup_user(request.form['username'],
                    request.form['password'], 
              request.form['password1'], request.form['name'], 
              request.form['email'])     
    return render_template('signup.html', message=message, 
                result=result, username=request.form['username'])

  return render_template('signup.html', message='')

def confirm_user(username, code):
  result=False
  message=""
  try:
    response = cognitoclient.confirm_sign_up(
        ClientId=CLIENT_ID,
        Username=username,
        ConfirmationCode=code
      )
    result=True
    message="User confirmed"
  except ClientError as e:
    if e.response['Error']['Code'] == 'UserNotFoundException':
      result=False
      message="Can't Find user by Email"
    if e.response['Error']['Code'] == 'CodeMismatchException':
      result=False
      message="User Code Mismatch"
    if e.response['Error']['Code'] == 'ParamValidationError':
      result=False
      message="Param Validation Error"
    if e.response['Error']['Code'] == 'ExpiredCodeException':
      result=False
      message="Expired Code"
    if e.response['Error']['Code'] == 'NotAuthorizedException':
      result=False
      message="User already confirmed"
    print(e)
  return result,message

@application.route('/confirm-email', methods = ['GET', 'POST'])
def confirmemail():
  if request.method == 'POST':
    result,message=confirm_user(request.form['username'],
                    request.form['code'])     
    return render_template('confirmemail.html', message=message, 
                result=result, username=request.form['username'])
  else:
    username = request.args.get('username', None)  
    return render_template('confirmemail.html', message='', 
                            username=username)

def process_forgotpass(username):
  result=False
  message=""
  try:
    response = cognitoclient.forgot_password(ClientId=CLIENT_ID,
                   Username=username)
    result=True
    message="Password reset code sent to registered email"
  except ClientError as e:
    if e.response['Error']['Code'] == 'UserNotFoundException':
      result=False
      message="Can't Find user by Email"
    if e.response['Error']['Code'] == 'ParamValidationError':
      result=False
      message="Param Validation Error"
    if e.response['Error']['Code'] == 'LimitExceededException':
      result=False
      message="Attempt limit exceeded, please try after some time"
    print(e)
  return result,message

@application.route('/forgot-password', methods = ['GET', 'POST'])
def forgotpass():
  if request.method == 'POST':
    result,message=process_forgotpass(request.form['username'])     
    return render_template('forgotpassword.html', message=message, 
                result=result, username=request.form['username'])
  else: 
    return render_template('forgotpassword.html', message='')


def process_resetpass(username, password, password1, code):
  print "resetting password"
  result=False
  message=""
  if password!=password1:
    result=False
    message="Passwords do not match"
    return result,message
  else:
    try:
      response=cognitoclient.confirm_forgot_password(ClientId=CLIENT_ID,
                           Username=username,
                           ConfirmationCode=code,
                           Password=password)
      result=True
      message="Password reset successful"      
    except ClientError as e:
      result=False
      if e.response['Error']['Code'] == 'UserNotFoundException':
        result=False
        message="Can't Find user by Email"
      if e.response['Error']['Code'] == 'CodeMismatchException':
        result=False
        message="User Code Mismatch"
      if e.response['Error']['Code'] == 'ParamValidationError':
        result=False
        message="Param Validation Error"
      if e.response['Error']['Code'] == 'ExpiredCodeException':
        result=False
        message="Expired Code"
      print(e)
    
    return result,message

@application.route('/reset-password', methods = ['GET', 'POST'])
def resetpass():
  if request.method == 'POST':
    result,message=process_resetpass(request.form['username1'], 
                    request.form['password'], request.form['password1'], 
                    request.form['code'])    

    return render_template('forgotpassword.html', message=message, 
                resetresult=result, username=request.form['username1'])
  else: 
    return render_template('forgotpassword.html', message='')

if __name__ == '__main__':
  application.run(debug=True, host="0.0.0.0", port=5000)
