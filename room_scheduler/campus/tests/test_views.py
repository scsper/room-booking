from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from campus.models import Room
from campus.models import Attribute


class CampusViewTests(TestCase):

	def setUp(self):
		""" create some rooms """
		Room.objects.create(name="Gym")
		Room.objects.create(name="Sanctuary")
		Room.objects.create(name="Fellowship Hall")


	def test_rooms_exist(self):
		""" all of the created rooms should be displayed in a list """

		response = self.client.get(reverse('campus:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Gym")
		self.assertContains(response, "Sanctuary")
		self.assertContains(response, "Fellowship Hall")


class AttributeViewTests(TestCase):

	def setUp(self):
		Attribute.objects.create(name="Piano")
		Attribute.objects.create(name="Speakers")

	def test_attributes_exist(self):
		""" all of the attributes should be displayed in a checklist """

		response = self.client.get(reverse('campus:attributes'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Piano")
		self.assertContains(response, "Speakers")

		
class NonExistenceViewTests(TestCase):

	def test_no_rooms_exist(self):
		"""
		when no rooms exist the page should display 
		'No rooms are available'
		"""

		response = self.client.get(reverse('campus:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No rooms are available")

	def test_no_attributes_exist(self):
		"""
		when no attributes exist the page should display 
		'No attributes are listed'
		"""

		response = self.client.get(reverse('campus:attributes'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No attributes are listed')


class SearchViewTests(TestCase):

	def setUp(self):
		""" create some rooms and link them with attributes"""
		Room.objects.create(name="Gym")
		Room.objects.create(name="Sanctuary")

		Attribute.objects.create(name="Piano")
		Attribute.objects.create(name="Speakers")
		Attribute.objects.create(name="Coffee Maker")
		Attribute.objects.create(name="Food")

		self.r1 = Room.objects.get(pk=1)
		self.r2 = Room.objects.get(pk=2)

		self.a1 = Attribute.objects.get(pk=1)
		self.a2 = Attribute.objects.get(pk=2)
		self.a3 = Attribute.objects.get(pk=3)
		self.a4 = Attribute.objects.get(pk=4)

		self.r1.attributes.add(self.a1, self.a2)
		self.r2.attributes.add(self.a2, self.a3)

	def test_search_by_none(self):
		""" searching by no attributes should return all rooms """
		response = self.client.get(reverse('campus:search'), {})
		self.assertEqual(response.status_code, 200)
		for room in Room.objects.all():
			self.assertContains(response, room.name)

	def test_search_by_one_get_none(self):
		response = self.client.get(reverse('campus:search'), {'attributes': self.a4.name})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No rooms are available")

	def test_search_by_one_get_one(self):
		response = self.client.get(reverse('campus:search'), {'attributes': self.a1.name})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.r1.name)

	def test_search_by_one_get_many(self):
		response = self.client.get(reverse('campus:search'), {'attributes': self.a2.name})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.r1.name)
		self.assertContains(response, self.r2.name)

	def test_search_by_many_get_none(self):
		response = self.client.get(reverse('campus:search'), {'attributes': self.a4.name, 'attributes': self.a3.name})
		self.assertEqual(response.status_code, 200)
		print "Response: ", response
		self.assertContains(response, "No rooms are available")

	# def test_search_by_many_get_one(self):

	# def test_search_by_many_get_many(self):

