from django import forms
from django.core.validators import EmailValidator, RegexValidator

class VendorForm(forms.Form):
    name = forms.CharField(max_length=100,validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Name must contain only letters and spaces')])
    email = forms.EmailField(validators=[EmailValidator(message='Invalid email format')])
    contact = forms.CharField(max_length=10,validators=[RegexValidator(regex='^\d{10}$', message='Contact must be a 10-digit number')])

class VendorProfileForm(forms.Form):
    name = forms.CharField(max_length=100,validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Name must contain only letters and spaces')])
    email = forms.EmailField(validators=[EmailValidator(message='Invalid email format')])
    contact = forms.CharField(max_length=10,validators=[RegexValidator(regex='^\d{10}$', message='Contact must be a 10-digit number')])
    whatsapp_no = forms.CharField(max_length=10, validators=[RegexValidator(regex='^\d{10}$', message='WhatsApp Number must be a 10-digit number')])
