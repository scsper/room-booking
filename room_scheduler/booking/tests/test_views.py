from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from datetime import timedelta
import datetime
import pytz

from booking.models import Series, Event, Frequency, InfinitelyRecurring
from campus.models import Room, Attribute
from booking.forms import CreateEventForm



class DetailViewTests(TestCase):
	def setUp(self):
		""" create some events to display"""
		self.r1 = Room.objects.create(name='Gym')

		self.time_now = datetime.datetime.utcnow()
		self.time_now = self.time_now.replace(tzinfo=pytz.utc)

		self.event1 = Event.objects.create(name='Deacon Meeting',
			setupStartTime = self.time_now + timedelta(days=1),
			eventStartTime = self.time_now + timedelta(days=1, minutes=30),
			eventEndTime = self.time_now + timedelta(days=1, hours=3),
			teardownEndTime = self.time_now + timedelta(days=1, hours=3, minutes=30))
		self.event2 = Event.objects.create(name='Basketball Game',
			setupStartTime = self.time_now + timedelta(days=2),
			eventStartTime = self.time_now + timedelta(days=2, minutes=30),
			eventEndTime = self.time_now + timedelta(days=2, hours=3),
			teardownEndTime = self.time_now + timedelta(days=2, hours=3, minutes=30))

		self.event1.rooms.add(self.r1)
		self.event2.rooms.add(self.r1)

	def test_events_displayed(self):
		response = self.client.get(reverse('booking:detail', args={self.r1.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, 'No events listed for this room')
		self.assertContains(response, 'Deacon Meeting')
		self.assertContains(response, 'Basketball Game')

	def test_title_display_correct(self):
		response = self.client.get(reverse('booking:detail', args={self.r1.pk}))
		self.assertContains(response, 'Gym Events')


class CreateEventViewTests(TestCase):
	def setUp(self):
		self.r1 = Room.objects.create(name='Gym')
		self.a1 = Attribute.objects.create(name="Projector")
		self.a2 = Attribute.objects.create(name="Piano")

		self.r1.attributes.add(self.a1, self.a2)

		self.time_now = datetime.datetime.now()
		self.time_now = self.time_now.replace(tzinfo=pytz.utc)


	def test_create_event_with_unfilled_form(self):
		""" Test that the form displays the view with the right template in the event that the form is unbound"""
		response = self.client.get(reverse('booking:create_event', args={self.r1.pk}))
		context = response.context
		status = response.status_code

		self.assertEqual(status, 200)
		self.assertTemplateUsed(response, 'booking/create_event.html')
		self.assertIsInstance(context['room'], Room)
		self.assertIsInstance(context['form'], CreateEventForm)
		# TODO: can't figure out how to test whether a form is unbound or not


	def test_create_event_with_incorrect_form(self):
		""" Test that the form does not redirect to a confirmation page if incorrect data is entered"""
		post_data = {
			'setupStartTime_0': ['2014-01-30'],
			'setupStartTime_1': ['5:00'],
			'eventStartTime_0': ['2014-01-30'],
			'eventStartTime_1': ['4:00'],
			'eventEndTime_0': ['2014-01-30'],
			'eventEndTime_1': ['6:00'],
			"teardownEndTime_0": ['2014-01-30'],
			"teardownEndTime_1": ['7:00'],
			'name': ['Incorrect Event'],
			'notes': ['The times are backwards!'],
			'rooms': ['1'],
			'attributes':['2']
		}

		response = self.client.post(reverse('booking:create_event', args={self.r1.pk}),  data=post_data)
		context = response.context
		status = response.status_code

		self.assertEqual(status, 200)
		self.assertTemplateUsed(response, 'booking/create_event.html')
		self.assertIsInstance(context['room'], Room)
		self.assertIsInstance(context['form'], CreateEventForm)


	def test_create_event_with_correct_form(self):
		""" Test that the form redirects to a confirmation page if the correct data is entered"""
		post_data = {
			'setupStartTime_0': ['2017-01-30'],
			'setupStartTime_1': ['4:00'],
			'eventStartTime_0': ['2017-01-30'],
			'eventStartTime_1': ['5:00'],
			'eventEndTime_0': ['2017-01-30'],
			'eventEndTime_1': ['6:00'],
			"teardownEndTime_0": ['2017-01-30'],
			"teardownEndTime_1": ['7:00'],
			'name': 'Correct Event',
			'notes': ['Woohoo!'],
			'rooms': ['1'],
			'attributes':['2']
		}

		response = self.client.post(reverse('booking:create_event', args=[self.r1.pk]),  data=post_data)
		context = response.context
		status = response.status_code

		self.assertEqual(status, 302)

		# TODO: Find out which template should be asserted for
		# self.assertTemplateUsed(response, 'booking/detail.html')


class EditEventViewTests(TestCase):
	def setUp(self):
		self.r1 = Room.objects.create(name='Gym')

		self.time_now = datetime.datetime.utcnow()
		self.time_now = self.time_now.replace(tzinfo=pytz.utc)

		self.event1 = Event.objects.create(name='Deacon Meeting',
			setupStartTime = self.time_now + timedelta(days=1),
			eventStartTime = self.time_now + timedelta(days=1, minutes=30),
			eventEndTime = self.time_now + timedelta(days=1, hours=3),
			teardownEndTime = self.time_now + timedelta(days=1, hours=3, minutes=30))

		self.event1.rooms.add(self.r1)

		self.a1 = Attribute.objects.create(name="Projector")
		self.a2 = Attribute.objects.create(name="Piano")

		self.r1.attributes.add(self.a1, self.a2)


	def test_edit_event_with_correct_form(self):
		""" Test that the edit form changes the model if the correct data is entered"""
		post_data = {
			'setupStartTime_0': ['2017-01-30'],
			'setupStartTime_1': ['4:00'],
			'eventStartTime_0': ['2017-01-30'],
			'eventStartTime_1': ['5:00'],
			'eventEndTime_0': ['2017-01-30'],
			'eventEndTime_1': ['6:00'],
			"teardownEndTime_0": ['2017-01-30'],
			"teardownEndTime_1": ['7:00'],
			'name': ['Correct Event'],
			'notes': ['Woohoo!'],
			'rooms': ['1'],
			'attributes':['1']
		}

		response = self.client.post(reverse('booking:edit_event', args=[self.r1.pk, self.event1.pk]),  data=post_data)
		updatedEvent = Event.objects.get(pk=self.event1.pk)
		status = response.status_code

		self.assertEqual(status, 302)
		self.assertEqual(updatedEvent.name, "Correct Event")

		# TODO: Find out which template should be asserted for
		# self.assertTemplateUsed(response, 'booking/detail.html')


class NonExistenceTests(TestCase):
	def test_no_events_in_detail_view(self):
		r1 = Room.objects.create(name='Gym')
		response = self.client.get(reverse('booking:detail', args={r1.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Gym Events')
		self.assertContains(response, 'No events listed for this room')
