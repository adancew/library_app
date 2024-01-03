from django.urls import path, include


from user.views import (
    reader_dash_view, 
)

app_name = 'user'

urlpatterns = [
    #path('', reader_dash_view, name='user-dash'),
    path('dashboard/', reader_dash_view, name="user-dash"),
]
