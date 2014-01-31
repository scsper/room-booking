from django.db import models
import datetime
import pytz

from campus.models import Room, Attribute


class Event(models.Model):
    name = models.CharField(max_length=50)
    notes = models.CharField(max_length=500, blank=True)
    setupStartTime = models.DateTimeField()
    eventStartTime = models.DateTimeField()
    eventEndTime = models.DateTimeField()
    teardownEndTime = models.DateTimeField()
    attributes = models.ManyToManyField(Attribute)
    series = models.ForeignKey('Series', null=True, blank=True)
    rooms = models.ManyToManyField(Room, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=50)
    notes = models.CharField(max_length=500, blank=True)
    setupStartTime = models.DateTimeField()
    eventStartTime = models.DateTimeField()
    eventEndTime = models.DateTimeField()
    teardownEndTime = models.DateTimeField()
    attributes = models.ManyToManyField(Attribute, null=True, blank=True)
    rooms = models.ManyToManyField(Room, null=True, blank=True)

    def __unicode__(self):
        return self.name


class InfinitelyRecurring(models.Model):
    series = models.ForeignKey('Series', null=True, blank=True)
    frequency = models.ForeignKey('Frequency', null=True, blank=True)

    def __unicode__(self):
        return self.series.name


class Frequency(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

