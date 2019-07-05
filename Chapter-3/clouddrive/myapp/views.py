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
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from forms import LoginForm, UploadFileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from s3upload import *


def logout_view(request):
	logout(request)
	return redirect('/')
      

@login_required
def profile_view(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	username = request.user.username
	email = request.user.email
	fname = request.user.first_name
	lname = request.user.last_name
	form = PasswordChangeForm(request.POST)
	return render_to_response('profile.html',{'form': form, 'username': username, 'email': email, 'fname':fname, 'lname': lname}, context_instance=RequestContext(request))

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render_to_response('register.html',{'form': form}, context_instance=RequestContext(request))

def handle_uploaded_file(f,username):
	uploadfilename='media/' + f.name
	with open(uploadfilename, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

	upload_to_s3_bucket_path('abahga2013', username, uploadfilename)
	return uploadfilename


@login_required
def delete_view(request,filename):
	username = request.user.username
	delete_from_s3('abahga2013', username,filename)
	userfiles,totalsize = getuserfiles('abahga2013', username)
	limit=5000
	percentused = totalsize*100/limit
	return render_to_response('index.html',{'username':username,'userfiles': userfiles,'totalsize':totalsize,'limit':limit,'percentused':percentused}, context_instance=RequestContext(request))


@login_required
def upload_view(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			username = request.user.username
			outputfilename = handle_uploaded_file(request.FILES['myfilefield'],username)
			userfiles,totalsize = getuserfiles('abahga2013', username)
			limit=5000
			percentused = totalsize*100/limit
			return render_to_response('index.html',{'username':username,'userfiles': userfiles,'totalsize':totalsize,'limit':limit,'percentused':percentused}, context_instance=RequestContext(request))
	else:
		form = UploadFileForm() 
		username = request.user.username
	return render_to_response('upload.html',{'form': form,'username':username}, context_instance=RequestContext(request))


def home(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				username = request.user.username
				userfiles,totalsize = getuserfiles('abahga2013', username)
				limit=5000
				percentused = totalsize*100/limit
				return render_to_response('index.html',{'username':username,'userfiles': userfiles,'totalsize':totalsize,'limit':limit,'percentused':percentused}, context_instance=RequestContext(request))
	else:
		if request.user.is_authenticated():	
			username = request.user.username
			userfiles,totalsize = getuserfiles('abahga2013', username)
			limit=5000
			percentused = totalsize*100/limit
			return render_to_response('index.html',{'username':username,'userfiles': userfiles,'totalsize':totalsize,'limit':limit,'percentused':percentused}, context_instance=RequestContext(request))

	form = LoginForm() 
   	return render_to_response('login.html',{'form': form}, context_instance=RequestContext(request))

def process(request):
	return render_to_response('filemanager.html', {})


