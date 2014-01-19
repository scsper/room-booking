from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from datetime import timedelta
import datetime
import pytz

from booking.models import Series, Event, Frequency, InfinitelyRecurring
from campus.models import Room, Attribute


class DetailViewTests(TestCase):
	def setUp(self):
		""" create some events to display"""
		self.r1 = Room.objects.create(name='Gym')

		self.time_now = datetime.datetime.utcnow()
		self.time_now = self.time_now.replace(tzinfo=pytz.utc)

		self.event1 = Event.objects.create(name='Deacon Meeting',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))
		self.event2 = Event.objects.create(name='Basketball Game',
			setupTime = self.time_now + timedelta(days=2),
			eventTime = self.time_now + timedelta(days=2, minutes=30),
			teardownTime = self.time_now + timedelta(days=2, hours=3),
			endTime = self.time_now + timedelta(days=2, hours=3, minutes=30))

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

		self.series = Series.objects.create(name='series1',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))

	def test_title_display_correct(self):
		response = self.client.get(reverse('booking:create_event', args={self.r1.pk}))
		self.assertContains(response, 'Create an event for Gym')

	def test_attribute_input_display(self):
		response = self.client.get(reverse('booking:create_event', args={self.r1.pk}))
		self.assertContains(response, 'Room attributes needed for event:')
		self.assertContains(response, 'Projector')
		self.assertContains(response, 'Piano')

	def test_series_input_display(self):
		response = self.client.get(reverse('booking:create_event', args={self.r1.pk}))
		self.assertContains(response, 'Series:(Leave blank for none)')
		self.assertContains(response, 'series1')
		self.assertContains(response, 'Create a series')


# class CreateViewTests(TestCase):
# 	def setUp(self):


# 	def test_no_required_fields_filled(self):
# 	def test_some_required_fields_filled(self):
# 	def test_all_required_fields_filled_correct(self):
# 	def test_only_setup_date_entered(self):
# 	def test_all_dates_correctly(self):
# 	def test_one_date_wrong_format(self):
# 	def test_some_dates_wrong_format(self):
# 	def test_all_dates_wrong_format(self):
# 	def test_event_date_before_setup_date(self):



class NonExistenceTests(TestCase):
	def test_no_events_in_detail_view(self):
		r1 = Room.objects.create(name='Gym')
		response = self.client.get(reverse('booking:detail', args={r1.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Gym Events')
		self.assertContains(response, 'No events listed for this room')

	def test_no_series_in_create_event_view(self):
		r1 = Room.objects.create(name='Gym')
		response = self.client.get(reverse('booking:create_event', args={r1.pk}))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Series:(Leave blank for none)')
		self.assertContains(response, 'Create a series')
		self.assertEqual(len(r1.series_set.all()), 0)
