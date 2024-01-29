from django import forms

from shared.models import Account, Reader, Borrowing, Resource


reader_query = [reader.account_id for reader in Reader.objects.all()]

class ReaderChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name} ({obj.id})"
    
class BorrowingChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.id} ({obj.status})"
    
class ResourceChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.title} ({obj.id})"

class FeeForm(forms.Form):
    amount = forms.IntegerField(
        label='Kwota', 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        label='Powód', 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    date_issued = forms.DateField(
        label='Data obciążenia (format: rrrr-mm-dd)', 
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    is_paid = forms.BooleanField(
        label='Czy uiszczono?', 
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    date_paid = forms.DateField(
        label='Data uiszczenia (format: rrrr-mm-dd)', 
        input_formats=['%Y-%m-%d'], 
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )
    borrowing = BorrowingChoiceField(
        label='Wypożyczenie', 
        queryset=Borrowing.objects.all().order_by('id'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    resource = ResourceChoiceField(
        label='Zasób', 
        queryset=Resource.objects.all().order_by('title'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
class AddFeeForm(FeeForm):
    reader = ReaderChoiceField(
        label='Czytelnik', 
        queryset=Account.objects.filter(id__in=reader_query).order_by('last_name'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )