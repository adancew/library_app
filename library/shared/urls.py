from django.urls import path, include


from shared.views import (
    home_view, 
    librarian_dash_view,
    signin_view,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', signin_view, name='signin-view'),
    path('dashboard/', librarian_dash_view, name="librarian-dash"),
]
