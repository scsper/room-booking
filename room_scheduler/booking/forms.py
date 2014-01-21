from django.forms import ModelForm
from datetime import datetime

import pytz

from booking.models import Event, Series
from campus.models import Room, Attribute

class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['series']

    def clean(self):
        cleaned_data = super(CreateEventForm, self).clean() # should handle the basic validation like existence and format
        print cleaned_data

        setupTime = cleaned_data.get('setupTime')
        eventTime = cleaned_data.get('eventTime')
        teardownTime = cleaned_data.get('teardownTime')
        endTime = cleaned_data.get('endTime')

        setupDate = cleaned_data.get('setupDate')
        eventDate = cleaned_data.get('eventDate')
        teardownDate = cleaned_data.get('teardownDate')
        endDate = cleaned_data.get('endDate')

        setupDateTime = self.combine_datetime(setupDate, setupTime)
        eventDateTime = self.combine_datetime(eventDate, eventTime)
        teardownDateTime = self.combine_datetime(teardownDate, teardownTime)
        endDateTime = self.combine_datetime(endDate, endTime)

        self.verify_order(setupDateTime, eventDateTime, teardownDateTime, endDateTime)
        self.verify_future(setupDateTime)


    def combine_datetime(self, date, time):
        print date
        print time
        combinedDateTime = datetime.strptime(date + " " + time, "%m-%d-%Y %I:%M %p")
        combinedDateTime = combinedDateTime.replace(tzinfo=pytz.utc)
        return combinedDateTime


    def verify_order(self, setup, event, teardown, end):
        """ question: why date and time?  couldn't we do it based solely on time? """
        if(setup.date() > event.date()):
            raise forms.ValidationError("Setup date cannot be after the event date.")
        if(event.date() > teardown.date()):
            raise forms.ValidationError("Event date cannot be after teardown date.")
        if(teardown.date() > end.date()):
            raise forms.ValidationError("Teardown date cannot be after end date.")

        if(setup > event):
            raise forms.ValidationError("Setup time cannot be after the event time.")
        if(event > teardown or (teardown - event).seconds == 0): # does teardown == event work?
            raise forms.ValidationError("Event time cannot be after teardown time.")
        if(teardown > end):
            raise forms.ValidationError("Teardown time cannot be after end time.")


    def verify_future(self, time):
        """Check times are in the future"""
        timeNow = datetime.now()
        timeNow = timeNow.replace(tzinfo=pytz.utc)
        if(time < timeNow):
            raise forms.ValidationError("Event must be in the future.")
