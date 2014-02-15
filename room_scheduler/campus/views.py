from django.shortcuts import render, redirect

from campus.models import Room, Attribute

def index(request):
    rooms = Room.objects.all()
    attributes = Attribute.objects.all()

    return render(request, 'campus/index.html', {'rooms': rooms, 'attributes': attributes})

def search(request):
    if request.GET.get('reset'):
        return redirect('/campus/search')

    attributes = request.GET.getlist('attributes')
    occupancy = request.GET.get('occupancy', '0')

    rooms = Room().search(occupancy, attributes)

    return render(request, 'campus/index.html', {'rooms': rooms, 'attributes': Attribute.objects.all()})


