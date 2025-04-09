from django.contrib import admin
from .models import Locations

@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('lname', 'address')
