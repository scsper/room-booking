from django.forms import ModelForm
from django.forms import ValidationError

from datetime import datetime
from django.forms import widgets

import pytz

from booking.models import Event, Series
from campus.models import Room, Attribute

class CreateEventForm(ModelForm):
    """ TODO: How to force a field to be required? """
    class Meta:
        model = Event
        exclude = ['series']


    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.fields['setupTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['eventTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['teardownTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['endTime'].widget = widgets.SplitDateTimeWidget()


    def save(self, commit=True):
        data = self.cleaned_data
        series = self.create_series(data)

        formModel = super(CreateEventForm, self).save(commit=commit)

        # add series as a foreign key on the model
        formModel.series = series
        formModel.save()

        return formModel


    def create_series(self, data):
        series = Series.objects.create(name=data['name'], \
            notes=data['notes'], \
            setupTime=data['setupTime'], \
            eventTime=data['eventTime'], \
            teardownTime=data['teardownTime'], \
            endTime=data['endTime'])

        # have to save the model first before adding many to many fields
        series.save()

        for room in data['rooms']:
            series.rooms.add(room)

        for attribute in data['attributes']:
            series.attributes.add(attribute)

        series.save()

        return series


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
        if(setup > event):
            raise ValidationError("Setup time cannot be after the event time.")
        if(event > teardown):
            raise ValidationError("Event time cannot be after the teardown time.")
        if(teardown > end):
            raise ValidationError("Teardown time cannot be after the end time.")


    def verify_future(self, time):
        """Check times are in the future"""
        timeNow = datetime.now()
        timeNow = timeNow.replace(tzinfo=pytz.utc)

        if(time < timeNow):
            raise ValidationError("Event must be in the future.")
