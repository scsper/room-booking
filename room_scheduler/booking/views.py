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

	# Gather variables
	name = request.POST['name']
	setupTime = request.POST['setupTime']
	setupDate = request.POST['setupDate']
	eventTime = request.POST['eventTime']
	eventDate = request.POST['eventDate']
	teardownTime = request.POST['teardownTime']
	teardownDate = request.POST['teardownDate']
	endTime = request.POST['endTime']
	endDate = request.POST['endDate']
	attributes = request.POST.getlist('attributes')
	series = request.POST.get('series')

	# Check required fields are filled
	if( name == "" or setupTime == "" or eventTime == "" or teardownTime == "" or endTime == "" or setupDate == ""):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Enter all required fields"})

	# If dates are left blank set to same day as setup
	if(eventDate == ""):
		eventDate = setupDate
	if(teardownDate == ""):
		teardownDate = setupDate
	if(endDate == ""):
		endDate = setupDate

	# Check for AM/PM if not present 7:31-11:59 default am, 12:00-7:30 default pm
	timeStrs = [setupTime, eventTime, teardownTime, endTime]
	validTimeStrEnds = "am","pm"
	for i in range(len(timeStrs)):
		if not timeStrs[i].endswith(validTimeStrEnds):
			timeStrs[i] = timeStrs[i].rstrip()
			timeNum = timeStrs[i].partition(":")
			if(int(timeNum[0]) <= 7 and int(timeNum[2]) <= 30):
				timeStrs[i] = timeStrs[i] + " am"
			else:
				timeStrs[i] = timeStrs[i] + " pm"

	print timeStrs


	# Create times from strings and check if improperly formatted
	try:
		dtSetupTime = datetime.strptime(setupDate + " " + setupTime, "%m-%d-%Y %H:%M %p")
		dtEventTime = datetime.strptime(eventDate + " " + eventTime, "%m-%d-%Y %H:%M %p")
		dtTeardownTime = datetime.strptime(teardownDate + " " + teardownTime, "%m-%d-%Y %H:%M %p")
		dtEndTime = datetime.strptime(endDate + " " + endTime, "%m-%d-%Y %H:%M %p")
	except (ValueError):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Enter dates and times correctly"})

	# Make times aware
	dtSetupTime = dtSetupTime.replace(tzinfo=pytz.utc)
	dtEventTime = dtEventTime.replace(tzinfo=pytz.utc)
	dtTeardownTime = dtTeardownTime.replace(tzinfo=pytz.utc)
	dtEndTime = dtEndTime.replace(tzinfo=pytz.utc)

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
