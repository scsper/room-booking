from django.forms import ModelForm
from django.forms import ValidationError

from datetime import datetime
from django.forms import widgets

import pytz

from booking.models import Event, Series
from campus.models import Room, Attribute

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['series']


    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['setupStartTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['eventStartTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['eventEndTime'].widget = widgets.SplitDateTimeWidget()
        self.fields['teardownEndTime'].widget = widgets.SplitDateTimeWidget()


    def clean(self):
        cleaned_data = super(EventForm, self).clean() # should handle the basic validation like existence and format

        setupStartTime = cleaned_data.get('setupStartTime')
        eventStartTime = cleaned_data.get('eventStartTime')
        eventEndTime = cleaned_data.get('eventEndTime')
        teardownEndTime = cleaned_data.get('teardownEndTime')

        if(not setupStartTime or not eventStartTime or not eventEndTime or not teardownEndTime):
            raise ValidationError("A required time field was null")

        self.verify_order(setupStartTime, eventStartTime, eventEndTime, teardownEndTime)
        self.verify_future(setupStartTime)

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



class CreateEventForm(EventForm):
    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)


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
            setupStartTime=data['setupStartTime'], \
            eventStartTime=data['eventStartTime'], \
            eventEndTime=data['eventEndTime'], \
            teardownEndTime=data['teardownEndTime'])

        # have to save the model first before adding many to many fields
        series.save()

        for room in data['rooms']:
            series.rooms.add(room)

        for attribute in data['attributes']:
            series.attributes.add(attribute)

        series.save()

        return series


class EditEventForm(EventForm):
    def __init__(self, *args, **kwargs):
        super(EditEventForm, self).__init__(*args, **kwargs)



