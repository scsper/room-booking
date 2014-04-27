from django import forms
from django.forms import Form
from django.forms import widgets

from campus.models import Room, Attribute
from booking.models import Event

class RoomSearchForm(Form):
	attributes = forms.MultipleChoiceField(required=False, choices=Attribute().get_choices())
	occupancy = forms.IntegerField(required=False, min_value=0)
	# startTime = forms.SplitDateTimeField(required=False)
	# endTime = forms.SplitDateTimeField(required=False)

	def __init__(self, *args, **kwargs):
		super(RoomSearchForm, self).__init__(*args, **kwargs)
		# self.fields['attributes'].widget = widgets.CheckboxInput(choices=Attribute.objects.get(pk=1).get_choices())
		self.fields['attributes'].widget = widgets.SelectMultiple(choices=Attribute().get_choices())

	def clean(self):
		cleaned_data = super(RoomSearchForm, self).clean() # should handle the basic validation like existence and format

		attributes = cleaned_data.get('attributes')
		occupancy = cleaned_data.get('occupancy')
		startTime = cleaned_data.get('startTime')
		endTime = cleaned_data.get('endTime')

		# self.verify_order(startTime, endTime)

		return cleaned_data


	def clean_occupancy(cleandata):
		occupancy = cleandata.cleaned_data.get('occupancy')

		if occupancy == None or occupancy == '':
			occupancy = 0
		else:
			occupancy = int(occupancy)

		return occupancy

	# def verify_order(self, start, end):
	# 	if(start > end):
	# 		raise ValidationError("Start Time must be before End Time")




	