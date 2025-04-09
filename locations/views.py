from django.shortcuts import render
from .models import Locations

def index(request):
    locations = Locations.objects.all()
    return render(request, 'locations/index.html', {'locations': locations})
