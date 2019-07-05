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

from django.db import models 
from django.contrib.auth.models import User 
from django.conf import settings 
 
class Department(models.Model): 
    name = models.CharField(verbose_name="Name",  
            max_length=1000,blank = True,null=True) 
     
    number = models.CharField(verbose_name="Number", 
             max_length=1000,blank = True,primary_key=True) 
              
    def __unicode__(self): 
        return str(self.name)+" - "+str(self.number) 
         
class Project(models.Model): 
    name = models.CharField(verbose_name="Name", 
            max_length=1000,blank = True,null=True) 
     
    number = models.CharField(verbose_name="Number", 
            max_length=1000,blank = True,primary_key=True) 
     
    def __unicode__(self): 
        return str(self.name)+" - "+str(self.number) 
        def project_ids(self): 
        return "project_"+str(self.id) 
 
class Employee (models.Model): 
     
    name = models.CharField(verbose_name="Name", 
            max_length=1000,blank = True,null=True) 
     
    number = models.CharField(verbose_name="Number", 
            max_length=1000,blank = True,primary_key=True)     
     
    salary = models.CharField(verbose_name="Salary", 
            max_length=1000,blank = True,null=True) 
     
    department= models.ForeignKey(Department, null=True,blank=True,  
            related_name='departmentname', default="null") 
     
    project=models.ManyToManyField(Project,through='WorksOn') 
     
    def __unicode__(self): 
        return str(self.name)+" - "+str(self.number)+ 
                " - "+str(self.department.number) 
     
class WorksOn(models.Model): 
    employee = models.ForeignKey(Employee) 
    project = models.ForeignKey(Project)     
     
    def __unicode__(self): 
        return str(self.employee.name)+" - "+str(self.project.name) 
        
