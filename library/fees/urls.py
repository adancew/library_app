from django.urls import path

from fees.views import (
    index,
    details,
    register_payment,
    add,
    edit,
    delete
)

app_name = 'fees'

urlpatterns = [
    path('', index, name="index"),
    path('<int:fee_id>/details', details, name="details"),
    path('<int:fee_id>/register-payment', register_payment, name="register-payment"),
    path('add', add, name="add"),
    path('<int:fee_id>/edit', edit, name="edit"),
    path('<int:fee_id>/delete', delete, name="delete")
]