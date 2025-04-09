from django.contrib import admin
from .models import RSOs, StudentsRSOs, RSOEvents

@admin.register(RSOs)
class RSOsAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')

@admin.register(StudentsRSOs)
class StudentsRSOsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'rso')

@admin.register(RSOEvents)
class RSOEventsAdmin(admin.ModelAdmin):
    list_display = ('event', 'rso')
