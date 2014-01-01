from django.shortcuts import render

from campus.models import Room, Attribute

def index(request):
    rooms = Room.objects.all()
    attributes = Attribute.objects.all()

    return render(request, 'campus/index.html', {'rooms': rooms, 'attributes': attributes})

def search(request):
    searchAttributes = request.GET.getlist('attributes')
    attributes = Attribute.objects.all()
    rooms = Room.objects.all()

    for attribute in searchAttributes:
        rooms = rooms.filter(attributes__name=attribute)

    searchOccupancy = request.GET.get('occupancy', default=0)

    rooms = rooms.filter(occupancy__gte=searchOccupancy)

    return render(request, 'campus/index.html', {'rooms': rooms, 'attributes': attributes})


