from django.contrib import admin
from campus.models import Room, Attribute

class RoomAdmin(admin.ModelAdmin):
	list_display = ('name', 'occupancy', 'get_attributes')

class AttributeAdmin(admin.ModelAdmin):
	list_display = ('name', 'get_rooms')

admin.site.register(Room, RoomAdmin)
admin.site.register(Attribute, AttributeAdmin)


# Register your models here.
