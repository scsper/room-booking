from django.test import TestCase
from datetime import timedelta
import datetime
import pytz

from booking.models import Series, Event, Frequency, InfinitelyRecurring
from campus.models import Room, Attribute

class SeriesTestCase(TestCase):
    def setUp(self):
        self.time_now = datetime.datetime.now()
        self.time_now = self.time_now.replace(tzinfo=pytz.utc)

        self.series = Series.objects.create(name='series1',
            setupTime = self.time_now + timedelta(days=1),
            eventTime = self.time_now + timedelta(days=1, minutes=30),
            teardownTime = self.time_now + timedelta(days=1, hours=3),
            endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))


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
        a1 = Attribute.objects.create(name='Speakers')
        a2 = Attribute.objects.create(name='Piano')

        self.series.attributes.add(a1, a2)
        series_attrs = self.series.attributes.all()

        self.assertEqual(series_attrs[0], a1)
        self.assertEqual(series_attrs[1], a2)
        self.assertEqual(len(series_attrs), 2)


    def test_series_rooms(self):
        r1 = Room.objects.create(name='Gym')
        r2 = Room.objects.create(name='Charis')

        self.series.rooms.add(r1)
        self.series.rooms.add(r2)
        series_rooms = self.series.rooms.all()
        self.assertEqual(len(series_rooms),2)
        self.assertEqual(series_rooms[0], r1)
        self.assertEqual(series_rooms[1], r2)


    def test_series_events(self):
        e1 = Event.objects.create(name='event1',
            setupTime = self.time_now + timedelta(days=1),
            eventTime = self.time_now + timedelta(days=1, minutes=30),
            teardownTime = self.time_now + timedelta(days=1, hours=3),
            endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))
        e2 = Event.objects.create(name='event2',
            setupTime = self.time_now + timedelta(days=1),
            eventTime = self.time_now + timedelta(days=1, minutes=30),
            teardownTime = self.time_now + timedelta(days=1, hours=3),
            endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))

        self.series.event_set.add(e1, e2)
        series_events = self.series.event_set.all()

        self.assertEqual(series_events[0], e1)
        self.assertEqual(series_events[1], e2)
        self.assertEqual(len(series_events), 2)


    def test_series_infinitelyRecurring(self):
        f1 = Frequency.objects.create(name='freq1')
        infini1 = InfinitelyRecurring.objects.create(series_id=self.series.pk, frequency_id=f1.pk)
        infini2 = InfinitelyRecurring.objects.create(series_id=self.series.pk, frequency_id=f1.pk)
        series_infinis = self.series.infinitelyrecurring_set.all()

        self.assertIn(infini1, series_infinis)
        self.assertIn(infini2, series_infinis)
        self.assertEqual(len(series_infinis), 2)