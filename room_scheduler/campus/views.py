from django.shortcuts import render

from campus.models import Room, Attribute

def index(request):
    rooms = Room.objects.all()
    attributes = Attribute.objects.all()

    return render(request, 'campus/index.html', {'rooms': rooms, 'attributes': attributes})

def search(request):
    rooms = Room.objects.all()
    attributes = request.GET.getlist('attributes')
    
    if request.GET.get('occupancy') == '':
        occupancy = 0
    else:
        occupancy = request.GET.get('occupancy')

    rooms = rooms.filter(occupancy__gte=occupancy)

    for attribute in attributes:
        rooms = rooms.filter(attributes__name=attribute)

    return render(request, 'campus/index.html', {'rooms': rooms, 'attributes': Attribute.objects.all()})


