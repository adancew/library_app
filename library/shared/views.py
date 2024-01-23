from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from .models import Employee, Account
from .decorators import employee_required

def home_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    return render(request, "home.html", {}) 



def signin_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            switch_value = form.cleaned_data['UserType']
            
            if switch_value == 'Librarian':
                user = Account.objects.get(id=2)
                login(request, user)
                return redirect('accounts:librarian-dash')
            else:
                user = Account.objects.get(id=3)
                login(request, user)
                return redirect('user:user-dash')
    else:
        form = LoginForm()

    return render(request, 'signin.html', {'form': form})

def signout_view(request):
    logout(request)
    return render(request, 'home.html')


@login_required
@employee_required  # my decorator
def librarian_dash_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    
    return render(request, "librarian_dash.html", {}) 