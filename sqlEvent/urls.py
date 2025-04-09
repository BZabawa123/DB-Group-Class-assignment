# sqlEvent/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Make the accounts app the root URL.
    path('', include('accounts.urls')),
]
