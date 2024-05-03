from django import forms
from django.core.validators import EmailValidator, RegexValidator

class AdminForm(forms.Form):
    name = forms.CharField(max_length=100,validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Name must contain only letters and spaces')])
    email = forms.EmailField(validators=[EmailValidator(message='Invalid email format')])
    contact = forms.CharField(max_length=10,validators=[RegexValidator(regex='^\d{10}$', message='Contact must be a 10-digit number')])
    category= forms.CharField(required=True, widget=forms.Select(choices=()))
    
class AdminProfileForm(forms.Form):
    full_name = forms.CharField(max_length=100,validators=[RegexValidator(regex='^[a-zA-Z ]*$', message='Name must contain only letters and spaces')])
    # email = forms.EmailField(validators=[EmailValidator(message='Invalid email format')])
    contact = forms.CharField(max_length=10,validators=[RegexValidator(regex='^\d{10}$', message='Contact must be a 10-digit number')])
    event_name = forms.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', message='Shop name can only contain letters and spaces')])
    contact = forms.CharField( max_length=10, validators=[RegexValidator(r'^\d{10}$', message='Contact must be a 10-digit number')])
    whatsapp_no = forms.CharField(max_length=10, validators=[RegexValidator(regex='^\d{10}$', message='WhatsApp Number must be a 10-digit number')])
    about_event = forms.CharField(required=True, widget=forms.Textarea)
    address = forms.CharField(required=True, widget=forms.Textarea)
    city= forms.CharField(required=True, validators=[RegexValidator(r'^[a-zA-Z\s]*$', message='city name can only contain letters and spaces')])

    