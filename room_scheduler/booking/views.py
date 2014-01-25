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

def create_event(request, room_id):
	room = get_object_or_404(Room, pk=room_id)

	if request.method == "POST":
		form = CreateEventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('booking:detail', args=[room.id]))

	# # If event is reoccuring, add the series
	# if series is not None:
	#     event.series.add(series)
	else:
		form = CreateEventForm()

	# we errored if we came to this point
	return render(request, 'booking/create_event.html', {
		'form': form,
		'room': room
	})
