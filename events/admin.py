from django.contrib import admin
from .models import Event, EventCreation, Comments

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_date', 'start_time', 'end_time')

@admin.register(EventCreation)
class EventCreationAdmin(admin.ModelAdmin):
    list_display = ('event', 'admin', 'superadmin', 'privacy')

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'event', 'rating', 'timestamp')
