from django.test import TestCase
from datetime import timedelta
import datetime
import pytz
from datetime import datetime
from datetime import date
from datetime import time

from booking.models import Series, Event, Frequency, InfinitelyRecurring
from campus.models import Room, Attribute
from booking.forms import CreateEventForm


class CreateEventFormTest(TestCase):
    def setUp(self):
        self.r1 = Room.objects.create(name='Gym')
        self.a1 = Attribute.objects.create(name="Projector")
        self.a2 = Attribute.objects.create(name="Piano")

        self.year = 2017

        self.r1.attributes.add(self.a1, self.a2)
        self.postData = {
            'setupTime_0': date(self.year, 1, 30),
            'setupTime_1': time(4, 0),
            'eventTime_0': date(self.year, 1, 30),
            'eventTime_1': time(4, 15),
            'teardownTime_0': date(self.year, 1, 30),
            'teardownTime_1': time(4, 30),
            'endTime_0': date(self.year, 1, 30),
            'endTime_1': time(4, 45),
            'name': 'Correct Event',
            'notes': 'Yay!',
            'rooms': ["1"],
            'attributes': ["1", "2"]
        }


    def test_valid_data(self):
        form = CreateEventForm(data=self.postData)
        self.assertEquals(form.is_valid(), True)


    def test_setup_after_event_date(self):
        self.postData['setupTime_0'] = date(self.year, 3, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Setup time cannot be after the event time.")


    def test_setup_after_event_time(self):
        self.postData['setupTime_1'] = time(5, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Setup time cannot be after the event time.")


    def test_event_after_teardown_date(self):
        self.postData['eventTime_0'] = date(self.year, 3, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Event time cannot be after the teardown time.")


    def test_event_after_teardown_time(self):
        self.postData['eventTime_1'] = time(5, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Event time cannot be after the teardown time.")


    def test_teardown_after_end_date(self):
        self.postData['teardownTime_0'] = date(self.year, 3, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Teardown time cannot be after the end time.")


    def test_teardown_after_end_time(self):
        self.postData['teardownTime_1'] = time(5, 15)

        form = CreateEventForm(data=self.postData)

        self.assertEquals(form.is_valid(), False)
        self.assertEquals(form.errors['__all__'][0], "Teardown time cannot be after the end time.")


    def test_event_date_not_in_future(self):
        self.postData['setupTime_0'] = date(2012, 3, 15)

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

        self.assertEquals(series.setupTime, event.setupTime)
        self.assertEquals(series.eventTime, event.eventTime)
        self.assertEquals(series.teardownTime, event.teardownTime)
        self.assertEquals(series.endTime, event.endTime)
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




