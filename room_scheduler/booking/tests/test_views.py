from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from datetime import timedelta
import datetime

from booking.models import Series, Event, Frequency, InfinitelyRecurring
from campus.models import Room, Attribute


class DetailViewTests(TestCase):
	def setUp(self):
		""" create some events to display"""
		self.r1 = Room.objects.create(name='Gym')

		self.time_now = datetime.datetime.now()

		self.event1 = Event.objects.create(name='Deacon Meeting',
			setupTime = self.time_now + timedelta(days=1), 
			eventTime = self.time_now + timedelta(days=1, minutes=30), 
			teardownTime = self.time_now + timedelta(days=1, hours=3), 
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30),
			room = self.r1)
		self.event2 = Event.objects.create(name='Basketball Game',
			setupTime = self.time_now + timedelta(days=2), 
			eventTime = self.time_now + timedelta(days=2, minutes=30), 
			teardownTime = self.time_now + timedelta(days=2, hours=3), 
			endTime = self.time_now + timedelta(days=2, hours=3, minutes=30),
			room = self.r1)

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



	def test_title_display_correct(self):
		response = self.client.get(reverse('booking:create_event', args={self.r1.pk}))
		self.assertContains(response, 'Creating Event for Gym')


class NonExistenceTests(TestCase):
	def test_no_events_in_detail_view(self):
		r1 = Room.objects.create(name='Gym')
		response = self.client.get(reverse('booking:detail', args={r1.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Gym Events')
		self.assertContains(response, 'No events listed for this room')
