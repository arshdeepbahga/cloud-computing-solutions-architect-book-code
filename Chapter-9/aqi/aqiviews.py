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

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, Permission, User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render
import json
import time
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import datetime
from dateutil.tz import tzoffset

AWS_KEY="<enter>"
AWS_SECRET="<enter>"
REGION="us-east-1"
dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

table = dynamodb.Table('AirQualityData')
table_output = dynamodb.Table('AirQualityOutput')

def home_page(request):
    now=int(time.time())
    timestampold=now-86400

    response = table_output.scan(
        FilterExpression=Attr('timestamp').gt(timestampold)
    )

    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-computed.html', variables)

def raw_data_page(request):
    now=int(time.time())
    timestampold=now-86400

    response = table.scan(
        FilterExpression=Attr('timestamp').gt(timestampold)
    )

    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-dashboard.html', variables)

def filter_data(request,asset_filter):
    now=int(time.time())
    timestampold=now-86400

    if asset_filter=='all':
        stationID=''
        response = table_output.scan(
            FilterExpression=Attr('timestamp').gt(timestampold)
        )
    elif asset_filter=='ST102':
        stationID='ST102'
        response = table_output.scan(
            FilterExpression=Key('stationID').eq(stationID) & 
                Attr('timestamp').gt(timestampold)
        )
    elif asset_filter=='ST105':
        stationID='ST105'
        response = table_output.scan(
            FilterExpression=Key('stationID').eq(stationID) & 
                Attr('timestamp').gt(timestampold)
        )
    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-computed.html',variables)

def filter_data_time(request,time_filter):
    timestampold=''
    now=int(time.time())
    if time_filter=='1':
        timestampold=now - 60
    elif time_filter=='2':
        timestampold=now - 900
    elif time_filter=='3':
        timestampold=now - 3600
    elif time_filter=='4':
        timestampold=now - 21600
    elif time_filter=='5':
        timestampold=now - 43200
    elif time_filter=='6':
        timestampold=now - 86400
            
    response = table_output.scan(
            FilterExpression=Attr('timestamp').gt(timestampold)
        )
    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-computed.html',variables)

def filter_raw_data(request,asset_filter):
    now=int(time.time())
    timestampold=now-86400

    if asset_filter=='all':
        stationID=''
        response = table.scan(
            FilterExpression=Attr('timestamp').gt(timestampold)
        )
    elif asset_filter=='ST102':
        stationID='ST102'
        response = table.scan(
            FilterExpression=Key('stationID').eq(stationID) & 
                Attr('timestamp').gt(timestampold)
        )
    elif asset_filter=='ST105':
        stationID='ST105'
        response = table.scan(
            FilterExpression=Key('stationID').eq(stationID) & 
                Attr('timestamp').gt(timestampold)
        )    
    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-dashboard.html',variables)

def filter_raw_data_time(request,time_filter):
    timestampold=''
    now=int(time.time())
    if time_filter=='1':
        timestampold=now - 60
    elif time_filter=='2':
        timestampold=now - 900
    elif time_filter=='3':
        timestampold=now - 3600
    elif time_filter=='4':
        timestampold=now - 21600
    elif time_filter=='5':
        timestampold=now - 43200
    elif time_filter=='6':
        timestampold=now - 86400
            
    response = table.scan(
            FilterExpression=Attr('timestamp').gt(timestampold)
        )
    items = response['Items']
    variables = RequestContext(request, {'items':items})
    return render_to_response('aqi-dashboard.html',variables)    

def dashboard_home(request):    
    variables = RequestContext(request, {})
    return render_to_response('aqi-dashboard.html', variables)


