from django import forms

class LoginForm(forms.Form):
    CHOICES = [
        ('Reader', 'Reader'),
        ('Librarian', 'Librarian'),
    ]
    UserType = forms.CharField(label='Log in as', widget=forms.RadioSelect(choices=CHOICES))