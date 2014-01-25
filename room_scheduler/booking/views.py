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
		print 'Raw Data: "%s"' % request.body
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('booking:detail', args=[room.id]))

	# Create the Event
	# event = Event.objects.create(name=name, notes=request.POST['notes'], setupTime=dtSetupTime, eventTime=dtEventTime, teardownTime=dtTeardownTime, endTime=dtEndTime)

	# Attach attributes to Event
	# for attribute in attributes:
	#     event.attributes.add(Attribute.objects.get(name=attribute))

	# # If event is reoccuring, add the series
	# if series is not None:
	#     event.series.add(series)

	# # Attach the event to the room
	# event.rooms.add(room)

	##        return HttpResponseRedirect(reverse('booking:detail', args=(room.id,)))
	else:
		form = CreateEventForm()

	# we errored if we came to this point
	return render(request, 'booking/create_event.html', {
		'form': form,
		'room': room
	})

    # return render(request, 'booking/create_event.html', {'room': room, 'attributes': room.attributes.all(), 'series': Series.objects.all()})

