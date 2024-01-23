from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from datetime import date, timedelta

from shared.decorators import employee_required
from .forms import EnterCodeForm, ScanCodeForm
from shared.models import Account, Reader, Card, Resource, Borrowing

# BORROW VIEWS ----------------------------------------------------------

@login_required
@employee_required 
def borrow_menu_view(request, *args, **kwargs):
    return render(request, "rentals/manage_rentals_menu.html", {}) 



@login_required
@employee_required
def scan_card(request, *args, **kwargs):
    # hard-coded value 1 of card-code (reader id: 3, name: R3name)
    if request.method == 'POST':
        form = ScanCodeForm(request.POST)
        
        if form.is_valid():
            if 'scan_ok' in request.POST:
                card_code = form.cleaned_data['Code']
                card = Card.objects.get(id=card_code)
                reader = Reader.objects.get(id=card.reader_id)
                account = Account.objects.get(id=reader.account_id)
                return redirect('rentals:reader-menu', account_id= account.id)
            else:
                form = ScanCodeForm()
                messages.error(request, "Wystąpił błąd")
                render(request, 'rentals/scan_card.html', {'form': form})
    else:
        form = ScanCodeForm()
        
    return render(request, 'rentals/scan_card.html', {'form': form})



@login_required
@employee_required
def enter_card(request, *args, **kwargs):
    if request.method == 'POST':
        form = EnterCodeForm(request.POST)
        if form.is_valid():
            try:
                card_code = form.cleaned_data['Code']
                card = Card.objects.get(id=card_code)
                reader = Reader.objects.get(id=card.reader_id)
                account = Account.objects.get(id=reader.account_id)
                return redirect('rentals:reader-menu', account_id= account.id)
            except:
                form = EnterCodeForm()
                messages.error(request, "Wystąpił błąd")
                render(request, 'rentals/enter_card.html', {'form': form})
            
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
    
    # hard-coded value 1 of resource-code (reader id: 3, name: R3name)
    if request.method == 'POST':
        form = ScanCodeForm(request.POST, initial=1)
        
        if form.is_valid():
            if 'scan_ok' in request.POST:
                resource_code = form.cleaned_data['Code']
                resource = Resource.objects.get(id=resource_code)
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

                return render(request, 'rentals/confirm_rental.html', {'form': form, 'account_id':account_id})
        
            else:
                form = ScanCodeForm()
                messages.error(request, "Wystąpił błąd")
                return render(request, 'rentals/scan_resource.html', {'form': form, 'account_id':account_id})
    else:
        form = ScanCodeForm()
        
    return render(request, 'rentals/scan_resource.html', {'form': form, 'account_id':account_id})


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

            return render(request, 'rentals/confirm_rental.html',  {'form': form, 'account_id':account_id})
            
    else:
        form = EnterCodeForm()

    return render(request, 'rentals/enter_resource.html', {'form': form})


# RETURN VIEWS ----------------------------------------------------------


@login_required
@employee_required 
def return_scan(request, *args, **kwargs):
    if request.method == 'POST':
        form = ScanCodeForm(request.POST, initial=1)
        
        if form.is_valid():
            if 'scan_ok' in request.POST:
                resource_code = form.cleaned_data['Code']
                resource = Resource.objects.get(id=resource_code)
                rental = Borrowing.objects.filter(resource__id=resource.id,
                                                  status="UNDERWAY")
                if(rental):
                    rental.update(status="RETURNED", date_returned=date.today())
                    return render(request, 'rentals/confirm_return.html', {'form': form})
        
                else:
                    form = ScanCodeForm()
                    messages.error(request, "Wystąpił błąd")
                    return render(request, 'rentals/scan_return.html', {'form': form})
            
            else:
                form = ScanCodeForm()
                messages.error(request, "Wystąpił błąd")
                return render(request, 'rentals/scan_return.html', {'form': form})
    else:
        form = ScanCodeForm()
        
    return render(request, 'rentals/scan_return.html', {'form': form})


    

@login_required
@employee_required
def return_enter(request, *args, **kwargs):
    if request.method == 'POST':
        form = EnterCodeForm(request.POST)
        if form.is_valid():
            try:
                resource_code = form.cleaned_data['Code']
                resource = Resource.objects.get(id=resource_code)
                rental = Borrowing.objects.filter(resource__id=resource.id, status="UNDERWAY")
                if(not rental): raise Exception # ugly, but works for now
                rental.update(status="RETURNED", date_returned=date.today())
                return render(request, 'rentals/confirm_return.html', {'form': form})
            except:
                form = EnterCodeForm()
                messages.error(request, "Wystąpił błąd")
                return render(request, 'rentals/enter_resource.html', {'form': form})
            
        else:
            form = EnterCodeForm()
            messages.error(request, "Wystąpił błąd")
            return render(request, 'rentals/enter_resource.html', {'form': form})
    else:
        form = EnterCodeForm()
        
    return render(request, 'rentals/enter_resource.html', {'form': form})
