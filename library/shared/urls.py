from django.urls import path, include
from django.contrib.auth import views as auth_views

from shared.views import (
    home_view, 
    librarian_dash_view,
    signin_view,
    signout_view,
    pick_login_view
)

app_name = 'accounts'

urlpatterns = [
    path('login/', signin_view, name='signin-view'),
    path('login-as/', pick_login_view, name='pick-login-view'),
    path('logout/', signout_view, name='signout-view'),
    path('dashboard/', librarian_dash_view, name="librarian-dash"),
]
