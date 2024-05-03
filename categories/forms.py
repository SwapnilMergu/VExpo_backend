from django import forms
from django.core.validators import RegexValidator

class CategoryForm(forms.Form):
    cname = forms.CharField(max_length=100,validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Name must contain only letters and spaces')])
