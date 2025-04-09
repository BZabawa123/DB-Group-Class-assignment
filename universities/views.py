from django.shortcuts import render
from .models import Universities

def index(request):
    universities = Universities.objects.all()
    return render(request, 'universities/index.html', {'universities': universities})
