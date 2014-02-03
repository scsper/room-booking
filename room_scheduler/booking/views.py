from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from datetime import datetime
import pytz

from booking.models import Event, Series
from campus.models import Room, Attribute

from booking.forms import CreateEventForm


def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'booking/detail.html', {'room': room})


def view_event(request, room_id, event_id):
	room = get_object_or_404(Room, pk=room_id)
	event = get_object_or_404(Event, pk=event_id)
	return render(request, 'booking/view_event.html', {'room': room, 'event': event})


def edit_event(request, room_id, event_id):
	room = get_object_or_404(Room, pk=room_id)
	event = get_object_or_404(Event, pk=event_id)

	if request.method == "POST":
		form = CreateEventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('booking:detail', args=[room.id]))
		else:
			print form.errors
	else:
		form = CreateEventForm(instance=event)

	return render(request, 'booking/edit_event.html', {
		'form': form,
		'room': room,
		'event': event
	})


def create_event(request, room_id):
	room = get_object_or_404(Room, pk=room_id)

	if request.method == "POST":
		form = CreateEventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('booking:detail', args=[room.id]))
	else:
		form = CreateEventForm()

	return render(request, 'booking/create_event.html', {
		'form': form,
		'room': room
	})
