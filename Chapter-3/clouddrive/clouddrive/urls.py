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

from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'myapp.views.home'),	
    url(r'^logout/$', 'myapp.views.logout_view'),
url(r'^register/$', 'myapp.views.register_view'),	
url(r'^profile/$', 'myapp.views.profile_view'),
url(r'^upload/$', 'myapp.views.upload_view'),
url(r'^delete/(?P<filename>[\w\. ]+)$', 'myapp.views.delete_view'),
    url(r'^process/$', 'myapp.views.process'),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),
url(r'^password/change/done/$', auth_views.password_change_done,  name='auth_password_change_done'),

)

