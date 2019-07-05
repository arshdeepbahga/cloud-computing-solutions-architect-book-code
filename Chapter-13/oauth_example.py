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

import httplib
import time
import oauth.oauth as oauth

SERVER = 'hostname'
PORT = 8080
REQUEST_TOKEN_URL = 'request_token'
ACCESS_TOKEN_URL = 'access_token'
AUTHORIZATION_URL = 'authorize'
CALLBACK_URL = 'request_token_ready'
RESOURCE_URL = 'photos'
CONSUMER_KEY = 'key'
CONSUMER_SECRET = 'secret'

class MyOAuthClient(oauth.OauthClient):
    def __init__(self, server, port=httplib.HTTP_PORT, request_token_url='', access_token_url='', authorization_url=''):
        self.server = server
        self.port = port
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.connection = httplib.HTTPConnection("%s:%d"% (self.server, self.port))

    def fetch_request_token(self, oauth_request):
        self.connection.request(oauth_request.http_method, self.request_token_url,
        headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        return oauth.OauthToken.from_string(response.read())

    def fetch_access_token(self, oauth_request):
        self.connection.request(oauth_request.http_method, self.access_token_url,
        headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        return oauth.OauthToken.from_string(response.read())

    def authorize_token(self, oauth_request):
        self.connection.request(oauth_request.http_method, oauth_request.to_url())
        response = self.connection.getresponse()
        return response.read()

    def access_resource(self, oauth_request):
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        self.connection.request('POST', RESOURCE_URL,
        body=oauth_request.to_postdata(), headers=headers)
        response = self.connection.getresponse()
        return response.read()
