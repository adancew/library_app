from django import forms

class EnterCodeForm(forms.Form):
    
    Code = forms.IntegerField(label='Wpisz kod')