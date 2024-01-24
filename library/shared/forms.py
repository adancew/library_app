from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django import forms

class LoginForm(forms.Form):
    username = UsernameField(label='Login:', widget=forms.TextInput())
    password = forms.CharField(label='Hasło:', widget=forms.PasswordInput())
    
