from django.shortcuts import render, redirect

from campus.models import Room, Attribute

from campus.forms import RoomSearchForm

def index(request):
    form = RoomSearchForm()
    rooms = Room.objects.all()
    attributes = Attribute.objects.all()

    return render(request, 'campus/index.html', {'form': form, 'rooms': rooms, 'attributes': attributes})

# def search(request):
#     if request.GET.get('reset'):
#         return redirect('/campus/search')

#     attributes = request.GET.getlist('attributes')
#     occupancy = request.GET.get('occupancy', '0')

#     rooms = Room().search(occupancy, attributes)

#     return render(request, 'campus/index.html', {'rooms': rooms, 'attributes': Attribute.objects.all()})

def search(request):
    if request.GET.get('reset'):
        return redirect('/campus/search')

    if request.method == 'GET':
        print request
        form = RoomSearchForm(request.GET)
        if form.is_valid():
            # form.save()
            print form.cleaned_data, "\n\n", form.cleaned_data.get('occupancy'), "\n\n"
            rooms = Room().search(form.cleaned_data.get('occupancy'), form.cleaned_data.get('attributes'))
            return render(request, 'campus/index.html', {'form': form, 'rooms': rooms})
    else:
        form = RoomSearchForm()
    rooms = Room.objects.all()

    return render(request, 'campus/index.html', {'form': form, 'rooms': rooms})


