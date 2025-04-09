from django.contrib import admin
from .models import Universities

@admin.register(Universities)
class UniversitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'number_of_students')
    search_fields = ('name',)
