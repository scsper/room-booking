from django.test import TestCase
from datetime import timedelta
import datetime
import pytz
from datetime import datetime
from datetime import date
from datetime import time
from django.utils import timezone

from booking.models import Series, Event, Frequency, InfinitelyRecurring
from campus.models import Room, Attribute
from booking.forms import CreateEventForm, EditEventForm


class CreateEventFormTest(TestCase):
    def setUp(self):
        self.r1 = Room.objects.create(name='Gym')
        self.a1 = Attribute.objects.create(name="Projector")
        self.a2 = Attribute.objects.create(name="Piano")

        self.year = 2017

        self.r1.attributes.add(self.a1, self.a2)
        self.postData = {
            'setupStartTime_0': date(self.year, 1, 30),
            'setupStartTime_1': time(4, 0),
            'eventStartTime_0': date(self.year, 1, 30),
            'eventStartTime_1': time(4, 15),
            'eventEndTime_0': date(self.year, 1, 30),
            'eventEndTime_1': time(4, 30),
            'teardownEndTime_0': date(self.year, 1, 30),
            'teardownEndTime_1': time(4, 45),
            'name': 'Correct Event',
            'notes': 'Yay!',
            'rooms': ["1"],
            'attributes': ["1", "2"]
        }


    def test_valid_data(self):
        form = CreateEventForm(data=self.postData)
        self.assertEquals(form.is_valid(), True)


    def test_setup_after_event_date(self):
        self.postData['setupStartTime_0'] = date(self.year, 3, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Setup time cannot be after the event time.")


    def test_setup_after_event_time(self):
        self.postData['setupStartTime_1'] = time(5, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Setup time cannot be after the event time.")


    def test_event_after_teardown_date(self):
        self.postData['eventStartTime_0'] = date(self.year, 3, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Event time cannot be after the teardown time.")


    def test_event_after_teardown_time(self):
        self.postData['eventStartTime_1'] = time(5, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Event time cannot be after the teardown time.")


    def test_teardown_after_end_date(self):
        self.postData['eventEndTime_0'] = date(self.year, 3, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Teardown time cannot be after the end time.")


    def test_teardown_after_end_time(self):
        self.postData['eventEndTime_1'] = time(5, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Teardown time cannot be after the end time.")


    def test_event_date_not_in_future(self):
        self.postData['setupStartTime_0'] = date(2012, 3, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Event must be in the future.")


    def test_empty_datetimes(self):
        self.postData = {
            'name': ['Correct Event'],
            'notes': ['Yay!'],
            'rooms': ['1'],
            'attributes':['2']
        }

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "A required time field was null")


    def test_event_is_created(self):
        form = CreateEventForm(data=self.postData)
        self.assertEquals(form.is_valid(), True)

        form.save()

        events = Event.objects.all()
        event = events[0]

        self.assertEquals(len(events), 1)
        self.assertEquals(event.name, "Correct Event")


    def test_series_is_created_for_new_event(self):
        form = CreateEventForm(data=self.postData)
        self.assertEquals(form.is_valid(), True)

        form.save()

        series = Series.objects.all()
        self.assertEquals(len(series), 1)
        self.assertEquals(series[0].name, "Correct Event")


    def test_series_data_matches_event_data(self):
        form = CreateEventForm(data=self.postData)
        self.assertEquals(form.is_valid(), True)

        form.save()

        series = Series.objects.all()[0]
        event = Event.objects.all()[0]

        self.assertEquals(series.setupStartTime, event.setupStartTime)
        self.assertEquals(series.eventStartTime, event.eventStartTime)
        self.assertEquals(series.eventEndTime, event.eventEndTime)
        self.assertEquals(series.teardownEndTime, event.teardownEndTime)
        self.assertEquals(series.name, event.name)
        self.assertEquals(series.notes, event.notes)
        self.assertEquals(series.rooms.all()[0], event.rooms.all()[0])
        self.assertEquals(series.attributes.all()[0], event.attributes.all()[0])
        self.assertEquals(series.attributes.all()[1], event.attributes.all()[1])



    def test_foreign_key_for_event_is_set(self):
        form = CreateEventForm(data=self.postData)
        self.assertEquals(form.is_valid(), True)

        form.save()

        series = Series.objects.all()[0]
        event = Event.objects.all()[0]

        self.assertEquals(event.series, series)




class EditEventFormTest(TestCase):
    def setUp(self):
        self.time_now = datetime.now()
        self.time_now = self.time_now.replace(tzinfo=pytz.utc)

        self.r1 = Room.objects.create(name='Gym')
        self.a1 = Attribute.objects.create(name="Projector")
        self.a2 = Attribute.objects.create(name="Piano")

        self.series = Series.objects.create(name='event',
            setupStartTime = self.time_now + timedelta(days=1),
            eventStartTime = self.time_now + timedelta(days=1, minutes=30),
            eventEndTime = self.time_now + timedelta(days=1, hours=3),
            teardownEndTime = self.time_now + timedelta(days=1, hours=3, minutes=30))

        self.event = Event.objects.create(name='event',
            setupStartTime = self.time_now + timedelta(days=1),
            eventStartTime = self.time_now + timedelta(days=1, minutes=30),
            eventEndTime = self.time_now + timedelta(days=1, hours=3),
            teardownEndTime = self.time_now + timedelta(days=1, hours=3, minutes=30),
            series = self.series)

        self.year = 2017

        self.r1.attributes.add(self.a1, self.a2)
        self.postData = {
            'setupStartTime_0': date(self.year, 1, 30),
            'setupStartTime_1': time(4, 0),
            'eventStartTime_0': date(self.year, 1, 30),
            'eventStartTime_1': time(4, 15),
            'eventEndTime_0': date(self.year, 1, 30),
            'eventEndTime_1': time(4, 30),
            'teardownEndTime_0': date(self.year, 1, 30),
            'teardownEndTime_1': time(4, 45),
            'name': 'Correct Event',
            'notes': 'Yay!',
            'rooms': ["1"],
            'attributes': ["1", "2"],
            'series': "following"
        }


    def test_edit_event(self):
        form = EditEventForm(data=self.postData, instance=self.event)
        self.assertEquals(form.is_valid(), True)

        form.save()

        self.assertEquals(self.event.name, "Correct Event")
        self.assertEquals(self.event.notes, "Yay!")

        # timezone.make_aware gets rid of the following exception:
        # TypeError: can't compare offset-naive and offset-aware datetimes
        self.assertEquals(self.event.setupStartTime, timezone.make_aware(datetime(self.year, 1, 30, 4, 0), timezone.get_default_timezone()))
        self.assertEquals(self.event.eventStartTime, timezone.make_aware(datetime(self.year, 1, 30, 4, 15), timezone.get_default_timezone()))
        self.assertEquals(self.event.eventEndTime, timezone.make_aware(datetime(self.year, 1, 30, 4, 30), timezone.get_default_timezone()))
        self.assertEquals(self.event.teardownEndTime, timezone.make_aware(datetime(self.year, 1, 30, 4, 45), timezone.get_default_timezone()))

        self.assertEquals(self.event.rooms.all()[0], self.r1)
        self.assertEquals(self.event.attributes.all()[0], self.a1)
        self.assertEquals(self.event.attributes.all()[1], self.a2)


    def test_edit_series(self):
        self.postData['series'] = "following"

        form = EditEventForm(data=self.postData, instance=self.event)
        self.assertEquals(form.is_valid(), True)

        form.save()

        self.assertEquals(self.series.name, "Correct Event")
        self.assertEquals(self.series.notes, "Yay!")

        self.assertEquals(self.series.setupStartTime, timezone.make_aware(datetime(self.year, 1, 30, 4, 0), timezone.get_default_timezone()))
        self.assertEquals(self.series.eventStartTime, timezone.make_aware(datetime(self.year, 1, 30, 4, 15), timezone.get_default_timezone()))
        self.assertEquals(self.series.eventEndTime, timezone.make_aware(datetime(self.year, 1, 30, 4, 30), timezone.get_default_timezone()))
        self.assertEquals(self.series.teardownEndTime, timezone.make_aware(datetime(self.year, 1, 30, 4, 45), timezone.get_default_timezone()))

        self.assertEquals(self.series.rooms.all()[0], self.r1)
        self.assertEquals(self.series.attributes.all()[0], self.a1)
        self.assertEquals(self.series.attributes.all()[1], self.a2)



