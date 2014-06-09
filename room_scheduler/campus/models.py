from django.db import models
from django.utils.http import base36_to_int

# Create your models here.
class Attribute(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    def get_rooms(self):
    	return ", ".join([room.name for room in self.room_set.all()])

    def get_choices(self):
        choices = []
        for attribute in Attribute.objects.all():
            choices.append((attribute, attribute.name))
        return choices


class Room(models.Model):
    name = models.CharField(max_length=50)
    occupancy = models.IntegerField(default=0)
    attributes = models.ManyToManyField(Attribute)

    def __unicode__(self):
        return self.name

    def get_attributes(self):
    	return ", ".join([attribute.name for attribute in self.attributes.all()])

    
