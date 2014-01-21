from django.test import TestCase
from datetime import timedelta
import datetime
import pytz

from booking.models import Series, Event, Frequency, InfinitelyRecurring
from campus.models import Room, Attribute


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
