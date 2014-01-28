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

        self.r1.attributes.add(self.a1, self.a2)


    def test_valid_data(self):
        postData = {
            'setupTime_0': date(2014, 1, 30),
            'setupTime_1': time(4, 0),
            'eventTime_0': date(2014, 1, 30),
            'eventTime_1': time(4, 15),
            'teardownTime_0': date(2014, 1, 30),
            'teardownTime_1': time(4, 30),
            'endTime_0': date(2014, 1, 30),
            'endTime_1': time(4, 45),
            'name': ['Incorrect Event'],
            'notes': ['The times are backwards!'],
            'rooms': ['1'],
            'attributes':['2']
        }

        form = CreateEventForm(data=postData)
        self.assertEquals(form.is_valid(), True)



