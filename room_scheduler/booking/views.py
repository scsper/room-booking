from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from datetime import datetime
import pytz

from booking.models import Event, Series
from campus.models import Room, Attribute

def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'booking/detail.html', {'room': room})

def create_event(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'booking/create_event.html', {'room': room, 'attributes': room.attributes.all(), 'series': Series.objects.all()})

def create(request, room_id):
	room = get_object_or_404(Room, pk=room_id)

	name = request.POST['name']
	setupTime = request.POST['setupTime']
	setupDate = request.POST['setupDate']
	eventTime = request.POST['eventTime']
	eventDate = request.POST['eventDate']
	teardownTime = request.POST['teardownTime']
	teardownDate = request.POST['teardownDate']
	endTime = request.POST['endTime']
	endDate = request.POST['endDate']

	if( name == "" or setupTime == "" or eventTime == "" or teardownTime == "" or endTime == "" or setupDate == "" or eventDate == "" or teardownDate == "" or endDate == ""):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Enter all required fields"})


	try:
		dtSetupTime = datetime.strptime(setupDate + " " + setupTime, "%m-%d-%Y %H:%M %p")
		dtEventTime = datetime.strptime(eventDate + " " + eventTime, "%m-%d-%Y %H:%M %p")
		dtTeardownTime = datetime.strptime(teardownDate + " " + teardownTime, "%m-%d-%Y %H:%M %p")
		dtEndTime = datetime.strptime(endDate + " " + endTime, "%m-%d-%Y %H:%M %p")
	except (ValueError):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Enter dates and times correctly"})

	dtSetupTime = dtSetupTime.replace(tzinfo=pytz.utc)
	dtEventTime = dtEventTime.replace(tzinfo=pytz.utc)
	dtTeardownTime = dtTeardownTime.replace(tzinfo=pytz.utc)
	dtEndTime = dtEndTime.replace(tzinfo=pytz.utc)

	attributes = request.POST.getlist('attributes')
	series = request.POST.get('series')

	event = Event.objects.create(name=name, notes=request.POST['notes'],
		setupTime=dtSetupTime, eventTime=dtEventTime, teardownTime=dtTeardownTime, endTime=dtEndTime)
	for attribute in attributes:
		event.attributes.add(Attribute.objects.get(name=attribute))
	if series is not None:
		event.series.add(series)

	event.rooms.add(room)
	print event

	return HttpResponseRedirect(reverse('booking:detail', args=(room.id,)))

# Create your views here.
