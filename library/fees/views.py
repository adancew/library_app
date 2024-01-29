from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shared.decorators import employee_required
from .utils import *
from .forms import FeeForm, AddFeeForm


@login_required
@employee_required
def index(request, *args, **kwargs):
    return render(request, 'fees/index.html', {'fees': get_fees()})

@login_required
@employee_required
def details(request, fee_id, *args, **kwargs):
    return render(request, 'fees/details.html', {'fee': get_fee_details(fee_id)})

@login_required
@employee_required
def register_payment(request, fee_id, *args, **kwargs):
    try:
        register_fee_payment(fee_id)
        messages.success(request, 'Uiszczenie opłaty zostało zarejestrowane')
    except:
        messages.error(request, 'Nie można zarejestrować uiszczenia opłaty')
    finally:
        return redirect('fees:index')

@login_required
@employee_required
def add(request, *args, **kwargs):
    if request.method == 'POST':
        form = AddFeeForm(request.POST)
        if form.is_valid():
            fee = add_fee(form)
            messages.success(request, 'Opłata została dodana')
            return redirect('fees:details', fee_id=fee.id)
    else:
        form = AddFeeForm()
    return render(request, 'fees/add.html', {'form': form})

@login_required
@employee_required
def edit(request, fee_id, *args, **kwargs):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            update_fee(fee_id, form)
            messages.success(request, 'Opłata została zaktualizowana')
            return redirect('fees:details', fee_id=fee_id)
    else:
        form = FeeForm(initial=get_fee_details(fee_id))
    return render(request, 'fees/edit.html', 
                  {'fee': get_fee_details(fee_id),
                   'form': form})

@login_required
@employee_required
def delete(request, fee_id, *args, **kwargs):
    try:
        delete_fee(fee_id)
        messages.success(request, 'Opłata została anulowana')
    except:
        messages.error(request, 'Nie można anulować opłaty')
    finally:
        return redirect('fees:index')
