from django.urls import path


from user.views import (
    index,
    renew
)

app_name = 'user'

urlpatterns = [
    path('dashboard/', index, name="user-dash"),
    path('<int:borrowing_id>/renew', renew, name="renew"),
]
