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



        self.event = Event.objects.create(name='event',
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
        r1 = Room.objects.create(name='Gym')
        r2 = Room.objects.create(name='Charis')

        self.event.rooms.add(r1, r2)
        event_rooms = self.event.rooms.all()
        self.assertEqual(len(event_rooms),2)
        self.assertEqual(event_rooms[0], r1)
        self.assertEqual(event_rooms[1], r2)

    def test_event_attributes(self):
        a1 = Attribute.objects.create(name='Speakers')
        a2 = Attribute.objects.create(name='Piano')

        self.event.attributes.add(a1, a2)
        event_attrs = self.event.attributes.all()
        self.assertEqual(event_attrs[0], a1)
        self.assertEqual(event_attrs[1], a2)
        self.assertEqual(len(event_attrs), 2)

    def test_events_series(self):
        s1 = Series.objects.create(name='series1',
            setupTime = self.time_now + timedelta(days=1),
            eventTime = self.time_now + timedelta(days=1, minutes=30),
            teardownTime = self.time_now + timedelta(days=1, hours=3),
            endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))

        s2 = Series.objects.create(name='series2',
            setupTime = self.time_now + timedelta(days=1),
            eventTime = self.time_now + timedelta(days=1, minutes=30),
            teardownTime = self.time_now + timedelta(days=1, hours=3),
            endTime = self.time_now + timedelta(days=1, hours=3, minutes=30))

        s1.event_set.add(self.event)
        self.assertEqual(s1.event_set.all()[0], self.event)
        self.assertNotIn(self.event, s2.event_set.all())
        s2.event_set.add(self.event)
        self.assertNotIn(self.event, s1.event_set.all())
        self.assertEqual(s2.event_set.all()[0], self.event)