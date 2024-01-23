from django.contrib import admin
from django.urls import path, include
from shared.views import home_view

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('', home_view, name='home'),
    path('accounts/', include('shared.urls')),
    path('user/', include('user.urls')),
    path('rentals/', include('rentals.urls')),
    path('resources/', include('resources.urls')),
]
