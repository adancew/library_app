from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist

from .models import Account, Reader, Employee 

def isReader(account_obj):
    try:
        obj = Reader.objects.get(account_id = account_obj.id)
        return obj != None
    except ObjectDoesNotExist:
        return False
    
def isEmployee(account_obj):
    try:
        obj = Employee.objects.get(account_id= account_obj.id)
        return obj != None
    except ObjectDoesNotExist:
        return False


def reader_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a reader,
    TODO redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda account: isReader(account),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def employee_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is an employee,
    TODO redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda account: isEmployee(account),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator