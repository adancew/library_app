from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from shared.decorators import reader_required
from .utils import RenewalLimitExceededException, get_user_borrowings, renew_borrowing

@login_required
@reader_required  # my decorator
def index(request, *args, **kwargs):
    return render(request, "user/user_dashboard.html", {'borrowings': get_user_borrowings(request.user)}) 

@login_required
@reader_required
def renew(request, borrowing_id, *args, **kwargs):
    try:
        renew_borrowing(borrowing_id)
        messages.success(request, 'Wypożyczenie zostało przedłużone', extra_tags='success')
    except RenewalLimitExceededException:
        messages.error(request, 'Nie można przedłużyć wypożyczenia - przekroczono limit 2 przedłużeń', extra_tags='failure')
    except Exception as e:
        messages.error(request, 'Wystąpił błąd - nie można przedłużyć wypożyczenia', extra_tags='failure')
    finally:
        return redirect('user:user-dash')