from django.contrib import admin
from .models import Employee, Reader, Account, Card, Resource, Book, Fee, Borrowing

# Register your models here.

admin.site.register(Employee)
admin.site.register(Reader)
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Resource)
admin.site.register(Book)
admin.site.register(Fee)
admin.site.register(Borrowing)