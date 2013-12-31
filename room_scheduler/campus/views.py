from django.shortcuts import render

from campus.models import Room, Attribute

def index(request):
    rooms = Room.objects.all()
    return render(request, 'campus/index.html', {'rooms': rooms})

def attributes(request):
    attributes = Attribute.objects.all()
    return render(request, 'campus/attributes.html', {'attributes': attributes})

def search(request):
    attributes = request.GET.getlist('attributes')
    rooms = Room.objects.all()

    for attribute in attributes:
        rooms = rooms.filter(attributes__name=attribute)

    return render(request, 'campus/search.html', {'attributes': attributes})
