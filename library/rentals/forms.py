from django import forms


class EnterCodeForm(forms.Form):
    Code = forms.IntegerField(label='Wpisz kod')

class ScanCodeForm(forms.Form):
    Code = forms.IntegerField(label='Skanuj kod', 
                              widget = forms.HiddenInput(), 
                              initial=1,
                              required = False,
                              )
    
    
