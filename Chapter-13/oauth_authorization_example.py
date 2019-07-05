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
import MyOAuthClient

def oauth_example():
    # setup
    client = MyOAuthClient(SERVER, PORT, REQUEST_TOKEN_URL,
    ACCESS_TOKEN_URL, AUTHORIZATION_URL)
    consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    signature_method_plaintext = oauth.OAuthSignatureMethod_PLAINTEXT()
    signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()

    # get request token
    print 'Obtain a request token ...'
    oauth_request =
    oauth.OAuthRequest.from_consumer_and_token(consumer,
    callback=CALLBACK_URL,
    http_url=client.request_token_url)
    oauth_request.sign_request(signature_method_plaintext, consumer, None)
    print 'REQUEST (via headers)'
    print 'parameters: %s' % str(oauth_request.parameters)
    token = client.fetch_request_token(oauth_request)
    print 'GOT'
    print 'key: %s' % str(token.key)
    print 'secret: %s' % str(token.secret)
    print 'callback confirmed? %s' %
    str(token.callback_confirmed)

    print 'Authorize the request token ...'
    oauth_request =
    oauth.OAuthRequest.from_token_and_callback(token=token,
    http_url=client.authorization_url)
    print 'REQUEST (via url query string)'
    print 'parameters: %s' % str(oauth_request.parameters)
    # this will actually occur only on some callback
    response = client.authorize_token(oauth_request)
    print 'GOT'
    print response
    # sad way to get the verifier
    import urlparse, cgi
    query = urlparse.urlparse(response)[4]
    params = cgi.parse_qs(query, keep_blank_values=False)
    verifier = params['oauth_verifier'][0]
    print 'verifier: %s' % verifier

    # get access token
    print 'Obtain an access token ...'
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=token,verifier=verifier, http_url=client.access_token_url)
    oauth_request.sign_request(signature_method_plaintext,consumer, token)
    print 'REQUEST (via headers)'
    print 'parameters: %s' % str(oauth_request.parameters)
    token = client.fetch_access_token(oauth_request)
    print 'GOT'
    print 'key: %s' % str(token.key)
    print 'secret: %s' % str(token.secret)

    # access some protected resources
    print 'Access protected resources ...'
    parameters = {'file': 'file.pdf', 'size': 'original'} 
    oauth_request =oauth.OAuthRequest.from_consumer_and_token(consumer, token=token, http_method='POST', http_url=RESOURCE_URL, parameters=parameters)
    oauth_request.sign_request(signature_method_hmac_sha1,consumer, token)
    print 'REQUEST (via post body)'
    print 'parameters: %s' % str(oauth_request.parameters)
    params = client.access_resource(oauth_request)
    print 'GOT'
    print 'non-oauth parameters: %s' % params

if __name__ == '__main__':
    oauth_example()
