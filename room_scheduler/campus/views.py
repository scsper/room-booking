from django.shortcuts import render

from campus.models import Room

def index(request):
    rooms = Room.objects.all()
    return render(request, 'campus/index.html', {'rooms': rooms})
