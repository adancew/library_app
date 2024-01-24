from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from .models import Employee, Account
from .decorators import employee_required

def home_view(request, *args, **kwargs):
    
    return render(request, "home.html", {}) 

def signin_view(request, *args, **kwargs):

    if request.user.is_authenticated:
        user = Account.objects.get(username=request.user)
        if Employee.objects.filter(account_id = user.id).exists():
            return redirect('accounts:librarian-dash')
        else:
            return redirect('user:user-dash')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data['username'],password=form.data['password'],)
            if user is not None:
                login(request, user)
                if Employee.objects.filter(account_id=user.id).exists(): 
                    return redirect('accounts:librarian-dash')
                else:
                    return redirect('user:user-dash')
            else:
                messages.error(request, "Podano nieprawidłowy login lub hasło.")
                
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def signout_view(request):
    logout(request)
    return render(request, 'home.html')


@login_required
@employee_required 
def librarian_dash_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, "librarian_dash.html", {}) 


def pick_login_view(request):
    return render(request, 'pick_login.html')



