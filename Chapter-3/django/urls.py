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

from django.conf.urls import patterns, include, url 
from myapp import views 
from django.contrib import admin 
 
admin.autodiscover() 
 
urlpatterns = patterns('', 
    url(r'$^\wedge$$', 'myapp.views.home', name='home'), 
    url(r'$^\wedge$employees/$', 'myapp.views.employees', name='employees'), 
    url(r'$^\wedge$employee/(?P<query>\textbackslash w+)/$', 'myapp.views.employeedetail'), 
    url(r'$^\wedge$department/(?P<query>\textbackslash w+)/$', 'myapp.views.departmentdetail'), 
    url(r'$^\wedge$project/(?P<query>\textbackslash w+)/$', 'myapp.views.projectdetail'), 
    url(r'$^\wedge$admin/doc/', include(django.contrib.admindocs.urls)), 
    url(r'$^\wedge$admin/', include(admin.site.urls)), 
)
