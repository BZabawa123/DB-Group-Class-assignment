from django.shortcuts import render
from .models import RSOs

def index(request):
    rsos = RSOs.objects.all()
    return render(request, 'rso_events/index.html', {'rsos': rsos})
