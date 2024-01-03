from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from shared.decorators import reader_required

@login_required
@reader_required  # my decorator
def reader_dash_view(request, *args, **kwargs):
    print(args, kwargs)
    print(request.user)
    
    return render(request, "user/user_dashboard.html", {}) 