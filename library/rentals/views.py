from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from datetime import date, timedelta

from shared.decorators import employee_required
from .forms import EnterCodeForm
from shared.models import Account, Reader, Card, Resource, Borrowing

# TODO data validation, handling not found exceptions, write fake scanning procedure

@login_required
@employee_required 
def borrow_menu_view(request, *args, **kwargs):
    return render(request, "rentals/manage_rentals_menu.html", {}) 


@login_required
@employee_required
def scan_card(request, *args, **kwargs):
    return render(request, "rentals/scan_card.html", {}) 


@login_required
@employee_required
def enter_card(request, *args, **kwargs):
    if request.method == 'POST':
        form = EnterCodeForm(request.POST)
        if form.is_valid():
            card_code = form.cleaned_data['Code']
            
            card = Card.objects.get(id=card_code)
            reader = Reader.objects.get(id=card.reader_id)
            account = Account.objects.get(id=reader.account_id)
            return redirect('rentals:reader-menu', account_id= account.id)
            
    else:
        form = EnterCodeForm()

    return render(request, 'rentals/enter_card.html', {'form': form})


@login_required
@employee_required
def reader_menu(request, account_id, *args, **kwargs):
    try:
        obj = Account.objects.get(id=account_id)
    except Reader.DoesNotExist:
        raise Http404

    context = {
        'object': obj
    }
    
    return render(request, 'rentals/borrow_reader_menu.html', context)


@login_required
@employee_required 
def scan_resource(request, account_id, *args, **kwargs):
    try:
        obj = Account.objects.get(id=account_id)
    except Reader.DoesNotExist:
        raise Http404
    
    context = {
        'object': obj
    }
    return render(request, "rentals/scan_resource.html", context) 


@login_required
@employee_required
def enter_resource(request, account_id, *args, **kwargs):
    if request.method == 'POST':
        form = EnterCodeForm(request.POST)
        if form.is_valid():
            resource_id = form.cleaned_data['Code']
            resource = Resource.objects.get(id=resource_id)
            reader = Reader.objects.get(account_id=account_id)
            
            new_rental = Borrowing(
                status='UNDERWAY', 
                date_borrowed = date.today(),
                date_due = date.today() + timedelta(days=14),
                date_returned=None,
                times_renewed = 0,
                reader = reader,
                resource = resource
                )
            new_rental.save()

            return render(request, 'rentals/confirm_rental.html')
            
    else:
        form = EnterCodeForm()

    return render(request, 'rentals/enter_resource.html', {'form': form})


