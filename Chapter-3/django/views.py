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
from django.shortcuts import render 
from django.shortcuts import redirect 
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from myapp.models import Department, Employee, Project, WorksOn 
 
def logout_view(request): 
	logout(request) 
	return redirect('/') 
 
def home(request): 
	if request.method == 'POST': 
		username = request.POST['username'] 
		password = request.POST['password'] 
		user = authenticate(username=username, password=password) 
		if user is not None: 
			if user.is_active: 
				login(request, user) 
				username = request.user.username 
				authorusername = str(request.user.username) 
 
	if request.user.is_authenticated(): 
		authorusername = str(request.user.username) 
		 
		employeecount = Employee.objects.all().count() 
		departmentcount = Department.objects.all().count() 
		projectcount = Project.objects.all().count() 
 
		return render_to_response('index.html',{ 
			'authorusername': authorusername,  'employeecount':employeecount, 
			 'departmentcount':departmentcount,  'projectcount':projectcount}, 
			  context_instance=RequestContext(request)) 
 
	return redirect('/accounts/login') 
	 
@login_required 
def employees(request): 
		if request.user.is_authenticated(): 
		authorusername = str(request.user.username) 
	employees = Employee.objects.all() 
	project_list=[] 
	len_e=len(employees) 
	for it in range(len(employees)): 
		temp1=employees[it].project.all()	 
		for items3 in temp1: 
			project_list.append((items3.name,employees[it].number)) 
	return render_to_response('employees.html',{ 
				'authorusername': authorusername,'employees':employees, 
				'len':len_e,'project_list':project_list},  
				context_instance=RequestContext(request)) 
	 
@login_required 
def employeedetail(request, query): 
	if request.user.is_authenticated(): 
		authorusername = str(request.user.username) 
 
	employee = Employee.objects.filter(number=query).get() 
	project_list=employee.project.all() 
	return render_to_response('employeedetail.html',{ 
		'authorusername': authorusername,'employee':employee, 
		'project_list':project_list},  
		context_instance=RequestContext(request)) 
 
@login_required 
def departmentdetail(request, query): 
	if request.user.is_authenticated(): 
		authorusername = str(request.user.username) 
 
	department = Department.objects.filter(number=query).get() 
	employee_count = Employee.objects.filter(department__pk=query).count() 
	return render_to_response('departmentdetail.html',{ 
		'authorusername': authorusername,'department':department, 
		'employee_count':employee_count},  
		context_instance=RequestContext(request)) 
 
@login_required 
def projectdetail(request, query): 
	if request.user.is_authenticated(): 
		authorusername = str(request.user.username) 
 
	project = Project.objects.filter(number=query).get() 
	employee_count = Employee.objects.filter(project__pk=query).count() 
	return render_to_response('projectdetail.html',{ 
		'authorusername': authorusername,'project':project, 
		'employee_count':employee_count},  
		context_instance=RequestContext(request))
