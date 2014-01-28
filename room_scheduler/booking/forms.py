from django.forms import ModelForm
from django.forms import ValidationError

from datetime import datetime
from django.forms import widgets

import pytz

from booking.models import Event, Series
from campus.models import Room, Attribute

class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['series']

    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.fields['setupTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['eventTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['teardownTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['endTime'].widget = widgets.SplitDateTimeWidget()


    def clean(self):
        cleaned_data = super(CreateEventForm, self).clean() # should handle the basic validation like existence and format

        setupTime = cleaned_data.get('setupTime')
        eventTime = cleaned_data.get('eventTime')
        teardownTime = cleaned_data.get('teardownTime')
        endTime = cleaned_data.get('endTime')

        if(not setupTime or not eventTime or not teardownTime or not endTime):
            raise ValidationError("A required time field was null")

        self.verify_order(setupTime, eventTime, teardownTime, endTime)
        self.verify_future(setupTime)

        return cleaned_data


    def verify_order(self, setup, event, teardown, end):
        """ question: why date and time?  couldn't we do it based solely on time? """
        # if(setup.date() > event.date()):
        #     raise ValidationError("Setup date cannot be after the event date.")
        # if(event.date() > teardown.date()):
        #     raise ValidationError("Event date cannot be after teardown date.")
        # if(teardown.date() > end.date()):
        #     raise ValidationError("Teardown date cannot be after end date.")
        if(setup > event):
            raise ValidationError("Setup time cannot be after the event time.")
        if(event > teardown or (teardown - event).seconds == 0): # does teardown == event work?
            raise ValidationError("Event time cannot be after teardown time.")
        if(teardown > end):
            raise ValidationError("Teardown time cannot be after end time.")


    def verify_future(self, time):
        """Check times are in the future"""
        timeNow = datetime.now()
        timeNow = timeNow.replace(tzinfo=pytz.utc)

        if(time < timeNow):
            raise ValidationError("Event must be in the future.")
