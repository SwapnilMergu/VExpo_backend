from django import forms
from .models import CustomUser

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

class EmailAuthenticationForm(AuthenticationForm):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [ 'email',  'vendor', 'admin', 'role', 'remember_token']
