from django.db import models

# Create your models here.
class Attribute(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=50)
    occupancy = models.IntegerField(default=0)
    attributes = models.ManyToManyField(Attribute)

    def __unicode__(self):
        return self.name

    def get_attributes(self):
    	return ", ".join([attribute.name for attribute in self.attributes.all()])


