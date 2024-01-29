from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shared.decorators import reader_required
from .utils import get_user_borrowings, renew_borrowing

@login_required
@reader_required  # my decorator
def index(request, *args, **kwargs):
    return render(request, "user/user_dashboard.html", {'borrowings': get_user_borrowings(request.user)}) 

def renew(request, borrowing_id, *args, **kwargs):
    try:
        renew_borrowing(borrowing_id)
        messages.success(request, 'Wypożyczenie zostało przedłużone')
    except:
        messages.error(request, 'Nie można przedłużyć wypożyczenia - przekroczono limit 2 przedłużeń')
    finally:
        return redirect('user:user-dash')