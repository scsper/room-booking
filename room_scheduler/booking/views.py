from django.shortcuts import render, get_object_or_404

from booking.models import Event
from campus.models import Room

def detail(request, room_id):
	room = get_object_or_404(Room, pk=room_id)
	return render(request, 'booking/detail.html', {'room': room})

def create_event(request, room_id):
	room = get_object_or_404(Room, pk=room_id)
	return render(request, 'booking/create_event.html', {'room': room})

# Create your views here.
