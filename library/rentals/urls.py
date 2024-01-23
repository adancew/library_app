from django.urls import path

from rentals.views import (
    # borrow views
    borrow_menu_view, 
    scan_card,
    enter_card,
    reader_menu,
    scan_resource,
    enter_resource,
    # return views
    return_scan,
    return_enter
)

app_name = 'rentals'

urlpatterns = [
    # borrow urls
    path('', borrow_menu_view, name="borrow-menu"),
    path('scan_card/', scan_card, name="scan-card"),
    path('enter_card/', enter_card, name="enter-card"),
    path('reader/<int:account_id>/', reader_menu, name="reader-menu"),
    path('reader/<int:account_id>/borrow_scan_resource/', scan_resource, name="scan-resource"),
    path('reader/<int:account_id>/borrow_enter_resource/', enter_resource, name="enter-resource"),
    # return urls
    path('return_scan/', return_scan, name="return-scan"),
    path('return_enter/', return_enter, name="return-enter"),

]
