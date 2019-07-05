'''
from django.db import models

class Document(models.Model):
    myfilefield = models.FileField(upload_to='documents/')
'''
