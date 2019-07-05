from django import forms

class UploadFileForm(forms.Form):
    myfilefield  = forms.FileField()
