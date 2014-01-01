from django.db import models

from campus.models import Room, Attribute

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=50)
    notes = models.CharField(max_length=500)
    setupTime = models.DateTimeField()
    eventTime = models.DateTimeField()
    teardownTime = models.DateTimeField()
    endTime = models.DateTimeField()
    attributes = models.ManyToManyField(Attribute)
    series = models.ForeignKey(Series)

    def __unicode__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=50)
    notes = models.CharField(max_length=500)
    setupTime = models.DateTimeField()
    eventTime = models.DateTimeField()
    teardownTime = models.DateTimeField()
    endTime = models.DateTimeField()
    attributes = models.ManyToManyField(Attribute)

    def __unicode__(self):
        return self.name


class InfinitelyRecurring(models.Model):
    series = models.ForeignKey(Series)
    frequency = models.ForeignKey(Frequency)

    def __unicode__(self):
        return self.series.name


class Frequency(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name