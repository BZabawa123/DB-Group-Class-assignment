from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='rso_events_index'),
]
