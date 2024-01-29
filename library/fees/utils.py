from datetime import datetime
from shared.models import Fee, Account, Reader

borrowing_status_dict = {
    "UNDERWAY": "w toku",
    "OVERKEPT": "przetrzymane",
    "RETURNED": "zwrócone",
    "LOST": "zgubione"
}

def get_user(account_id):
    user = Account.objects.get(id=account_id)
    return user

def fee_to_dict(fee):
    account = get_user(fee.reader.account_id)
    return {
        'id': fee.id,
        'amount': fee.amount,
        'reason': fee.reason,
        'date_issued': fee.date_issued,
        'is_paid': fee.is_paid,
        'date_paid': fee.date_paid,
        'reader': fee.reader,
        'reader_name': f'{account.first_name} {account.last_name}',
        'borrowing': fee.borrowing,
        'borrowing_info': f'{fee.borrowing.id} ({borrowing_status_dict[fee.borrowing.status]})' if fee.borrowing else '',
        'resource': fee.resource,
        'resource_info': f'{fee.resource.title} ({fee.resource.id})' if fee.resource else ''
    }

def get_fees():
    return [fee_to_dict(fee) for fee in Fee.objects.all()]

def get_fee_details(fee_id):
    fee = Fee.objects.get(id=fee_id)
    return fee_to_dict(fee)

def register_fee_payment(fee_id):
    fee = Fee.objects.get(id=fee_id)
    fee.is_paid = True
    fee.date_paid = datetime.today()
    fee.save()
    return fee

def add_fee(form):
    fee = Fee(
        amount=form.cleaned_data['amount'],
        reason=form.cleaned_data['reason'],
        date_issued=form.cleaned_data['date_issued'],
        is_paid=form.cleaned_data['is_paid'],
        date_paid=form.cleaned_data['date_paid'],
        reader=Reader.objects.get(account_id=form.cleaned_data['reader']),
        borrowing=form.cleaned_data['borrowing'],
        resource=form.cleaned_data['resource']
    )
    fee.save()
    return Fee.objects.latest('id')
    
def update_fee(fee_id, form):
    fee = Fee.objects.get(id=fee_id)
    fee.amount = form.cleaned_data['amount']
    fee.reason = form.cleaned_data['reason']
    fee.date_issued = form.cleaned_data['date_issued']
    fee.is_paid = form.cleaned_data['is_paid']
    fee.date_paid = form.cleaned_data['date_paid']
    fee.borrowing = form.cleaned_data['borrowing']
    fee.resource = form.cleaned_data['resource']
    fee.save()
    return fee
    
def delete_fee(fee_id):
    fee = Fee.objects.get(id=fee_id)
    fee.delete()
    return fee