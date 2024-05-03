from django import forms
from django.core.validators import RegexValidator,EmailValidator
from .models import Stalls

class StallForm(forms.Form):
    shop_name = forms.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\s]*$', message='Shop name can only contain letters and spaces')])
    email = forms.EmailField(validators=[EmailValidator(message="Enter email")])
    contact = forms.CharField( max_length=10, validators=[RegexValidator(r'^\d{10}$', message='Contact must be a 10-digit number')])
    cate_type = forms.CharField(max_length=100)
    # type = forms.ChoiceField(label='Type', choices=[('PDF', 'PDF'), ('Image', 'Image')])
    about_stall = forms.CharField(required=True, widget=forms.Textarea)
    address = forms.CharField(required=True, widget=forms.Textarea)
    city = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = Stalls