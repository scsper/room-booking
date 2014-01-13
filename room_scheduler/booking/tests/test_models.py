from django.test import TestCase
from datetime import timedelta
import datetime
import pytz

from booking.models import Series, Event, Frequency, InfinitelyRecurring
from campus.models import Room, Attribute


class EventTestCase(TestCase):
	def setUp(self):
		self.time_now = datetime.datetime.now()
		self.time_now = self.time_now.replace(tzinfo=pytz.utc)


		self.r1 = Room.objects.create(name='Gym')

		self.event = Event.objects.create(name='event',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30),
			room = self.r1)

		self.a1 = Attribute.objects.create(name='Speakers')
		self.a2 = Attribute.objects.create(name='Piano')

		self.s1 = Series.objects.create(name='series1',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))
		self.s2 = Series.objects.create(name='series2',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))

	def test_event_name(self):
		self.assertEqual(self.event.name, 'event')

	def test_event_notes_blank(self):
		self.assertEqual(self.event.notes, '')

	def test_event_notes_full(self):
		self.event.notes = 'this, whatever'
		self.assertEqual(self.event.notes, 'this, whatever')

	def test_event_setupTime(self):
		self.assertEqual(self.event.setupTime, self.time_now + timedelta(days=1))

	def test_event_eventTime(self):
		self.assertEqual(self.event.eventTime, self.time_now + timedelta(days=1, minutes=30))

	def test_event_teardownTime(self):
		self.assertEqual(self.event.teardownTime, self.time_now + timedelta(days=1, hours=3))

	def test_event_endTime(self):
		self.assertEqual(self.event.endTime, self.time_now + timedelta(days=1, hours=3, minutes=30))

	def test_event_room(self):
		self.assertEqual(self.event.room, self.r1)

	def test_event_attributes(self):
		self.event.attributes.add(self.a1, self.a2)
		event_attrs = self.event.attributes.all()

		self.assertEqual(event_attrs[0], self.a1)
		self.assertEqual(event_attrs[1], self.a2)
		self.assertEqual(len(event_attrs), 2)

	def test_events_series(self):
		self.s1.event_set.add(self.event)
		self.assertEqual(self.s1.event_set.all()[0], self.event)
		self.assertNotIn(self.event, self.s2.event_set.all())
		self.s2.event_set.add(self.event)
		self.assertNotIn(self.event, self.s1.event_set.all())
		self.assertEqual(self.s2.event_set.all()[0], self.event)



class SeriesTestCase(TestCase):
	def setUp(self):
		self.time_now = datetime.datetime.now()
		self.time_now = self.time_now.replace(tzinfo=pytz.utc)


		self.series = Series.objects.create(name='series1',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))

		self.a1 = Attribute.objects.create(name='Speakers')
		self.a2 = Attribute.objects.create(name='Piano')

		self.r1 = Room.objects.create(name='Gym')

		self.e1 = Event.objects.create(name='event1',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30),
			room = self.r1)
		self.e2 = Event.objects.create(name='event2',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30),
			room = self.r1)

	def test_series_name(self):
		self.assertEqual(self.series.name, "series1")

	def test_series_notes_blank(self):
		self.assertEqual(self.series.notes, '')

	def test_series_notes_fill(self):
		self.series.notes = 'this, this, that'
		self.assertEqual(self.series.notes, "this, this, that")

	def test_series_setupTime(self):
		self.assertEqual(self.series.setupTime, self.time_now + timedelta(days=1))

	def test_series_eventTime(self):
		self.assertEqual(self.series.eventTime, self.time_now + timedelta(days=1, minutes=30))

	def test_series_teardownTime(self):
		self.assertEqual(self.series.teardownTime, self.time_now + timedelta(days=1, hours=3))

	def test_series_endTime(self):
		self.assertEqual(self.series.endTime, self.time_now + timedelta(days=1, hours=3, minutes=30))

	def test_series_attributes(self):
		self.series.attributes.add(self.a1, self.a2)
		series_attrs = self.series.attributes.all()

		self.assertEqual(series_attrs[0], self.a1)
		self.assertEqual(series_attrs[1], self.a2)
		self.assertEqual(len(series_attrs), 2)

	def test_series_events(self):
		self.series.event_set.add(self.e1, self.e2)
		series_events = self.series.event_set.all()

		self.assertEqual(series_events[0], self.e1)
		self.assertEqual(series_events[1], self.e2)
		self.assertEqual(len(series_events), 2)

	def test_series_infinitelyRecurring(self):
		f1 = Frequency.objects.create(name='freq1')
		infini1 = InfinitelyRecurring.objects.create(series_id=self.series.pk, frequency_id=f1.pk)
		infini2 = InfinitelyRecurring.objects.create(series_id=self.series.pk, frequency_id=f1.pk)
		series_infinis = self.series.infinitelyrecurring_set.all()

		self.assertIn(infini1, series_infinis)
		self.assertIn(infini2, series_infinis)
		self.assertEqual(len(series_infinis), 2)


class InfinitelyRecurringTestCase(TestCase):
	def setUp(self):
		self.time_now = datetime.datetime.now()
		self.time_now = self.time_now.replace(tzinfo=pytz.utc)

		self.s1 = Series.objects.create(name='series',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))
		self.f1 = Frequency.objects.create(name='freq')

		self.infini = InfinitelyRecurring.objects.create(series_id=self.s1.pk, frequency_id=self.f1.pk)

	def test_infinitelyRecurring_series(self):
		self.assertEqual(self.infini.series, self.s1)

	def test_infinitelyRecurring_frequency(self):
		self.assertEqual(self.infini.frequency, self.f1)


class FrequencyTestCase(TestCase):
	def setUp(self):
		self.time_now = datetime.datetime.now()
		self.time_now = self.time_now.replace(tzinfo=pytz.utc)

		self.freq = Frequency.objects.create(name='freq1')
		self.series = Series.objects.create(name='series',
			setupTime = self.time_now + timedelta(days=1),
			eventTime = self.time_now + timedelta(days=1, minutes=30),
			teardownTime = self.time_now + timedelta(days=1, hours=3),
			endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))
		self.infini1 = InfinitelyRecurring.objects.create(series_id=self.series.pk, frequency_id=self.freq.pk)
		self.infini2 = InfinitelyRecurring.objects.create(series_id=self.series.pk, frequency_id=self.freq.pk)

	def test_frequency_name(self):
		self.assertEqual(self.freq.name, 'freq1')

	def test_frequency_infinetlyRecurring(self):
		frequency_infinis = self.freq.infinitelyrecurring_set.all()

		self.assertIn(self.infini1, frequency_infinis)
		self.assertIn(self.infini2, frequency_infinis)
		self.assertEqual(len(frequency_infinis), 2)
