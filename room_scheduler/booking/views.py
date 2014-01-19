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

	# Check for AM/PM
	# if not present 7:31-11:59 default am, 12:00-7:30 default pm
	timeStrs = [setupTime, eventTime, teardownTime, endTime]
	validTimeStrEnds = "AM","PM"
	for i in range(len(timeStrs)):
		if not timeStrs[i].endswith(validTimeStrEnds):
			timeStrs[i] = timeStrs[i].rstrip()
			timeNum = timeStrs[i].partition(":")
			if int(timeNum[0]) == 7:
				if int(timeNum[2]) > 30:
					timeStrs[i] = timeStrs[i] + " AM"
				else:
					timeStrs[i] = timeStrs[i] + " PM"
			if int(timeNum[0]) > 7 and int(timeNum[0]) < 12:
				timeStrs[i] = timeStrs[i] + " AM"
			if int(timeNum[0]) < 7 or int(timeNum[0]) == 12:
				timeStrs[i] = timeStrs[i] + " PM"

	setupTime = timeStrs[0]
	eventTime = timeStrs[1]
	teardownTime = timeStrs[2]
	endTime = timeStrs[3]

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

	# Check dates in order
	if(dtEventTime.date() < dtSetupTime.date()):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Event Date cannot be before Setup Date"})
	if(dtEndTime.date() < dtTeardownTime.date()):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Teardown Date cannot be before End Date"})
	if(dtTeardownTime.date() < dtEventTime.date() or (dtTeardownTime.date() - dtEventTime.date()).day == 0):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Teardown Date must be after Event Date"})

	# Check times in order
	if(dtEventTime < dtSetupTime):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Event Time cannot be before Setup Time"})
	if(dtEndTime < dtTeardownTime):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Teardown Time cannot be before End Time"})
	if(dtTeardownTime < dtEventTime or (dtTeardownTime - dtEventTime).seconds == 0):
		return render(request, 'booking/create_event.html', 
			{'room': room, 'attributes': room.attributes.all(),
			'series': Series.objects.all(), 'error_message': "Teardown Time must be after Event Time"})

	# Check times are in the future

	# Create the Event
	event = Event.objects.create(name=name, notes=request.POST['notes'],
		setupTime=dtSetupTime, eventTime=dtEventTime, teardownTime=dtTeardownTime, endTime=dtEndTime)
	# Attach attributes to Event
	for attribute in attributes:
		event.attributes.add(Attribute.objects.get(name=attribute))
	# If event is reoccuring, add the series
	if series is not None:
		event.series.add(series)

	# Attach the event to the room
	event.rooms.add(room)
	print event

	return HttpResponseRedirect(reverse('booking:detail', args=(room.id,)))

# Create your views here.
