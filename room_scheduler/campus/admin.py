from django.contrib import admin
from campus.models import Room, Attribute

class RoomAdmin(admin.ModelAdmin):
	list_display = ('name', 'occupancy', 'get_attributes')

admin.site.register(Room, RoomAdmin)
admin.site.register(Attribute)


# Register your models here.
