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
		when no attributes exist the panel should display
		'No attributes are listed'
		"""
		response = self.client.get(reverse('campus:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No attributes are listed")


class AttributeSearchViewTests(TestCase):
	def setUp(self):
		""" create some rooms and link them with attributes"""
		Room.objects.create(name="Gym")
		Room.objects.create(name="Sanctuary")
		Room.objects.create(name="Charis")

		Attribute.objects.create(name="Piano")
		Attribute.objects.create(name="Speakers")
		Attribute.objects.create(name="Coffee Maker")
		Attribute.objects.create(name="Food")

		self.r1 = Room.objects.get(pk=1)
		self.r2 = Room.objects.get(pk=2)
		self.r3 = Room.objects.get(pk=3)

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
		self.assertNotContains(response, self.r1.name)
		self.assertNotContains(response, self.r2.name)
		self.assertNotContains(response, self.r3.name)


	def test_search_by_one_get_one(self):
		response = self.client.get(reverse('campus:search'), {'attributes': self.a1.name})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.r1.name)
		self.assertNotContains(response, self.r2.name)
		self.assertNotContains(response, self.r3.name)


	def test_search_by_one_get_many(self):
		response = self.client.get(reverse('campus:search'), {'attributes': self.a2.name})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, self.r1.name)
		self.assertContains(response, self.r2.name)
		self.assertNotContains(response, self.r3.name)


	def test_search_by_many_get_none(self):
		response = self.client.get(reverse('campus:search'), {'attributes': [self.a1.name, self.a3.name]})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No rooms are available")
		self.assertNotContains(response, self.r1.name)
		self.assertNotContains(response, self.r2.name)
		self.assertNotContains(response, self.r3.name)

	def test_search_by_many_get_one(self):
		response = self.client.get(reverse('campus:search'), {'attributes': [self.a3.name, self.a2.name]})

		self.assertContains(response, self.r2.name)
		self.assertNotContains(response, self.r1.name)
		self.assertNotContains(response, self.r3.name)

	def test_search_by_many_get_many(self):
		self.r3.attributes.add(self.a1, self.a2)
		response = self.client.get(reverse('campus:search'), {'attributes': [self.a1.name, self.a2.name]})

		self.assertContains(response, self.r1.name)
		self.assertContains(response, self.r3.name)
		self.assertNotContains(response, self.r2.name)


class OccupancySearchViewTests(TestCase):

	def setUp(self):
		Room.objects.create(name="Gym", occupancy=10)
		Room.objects.create(name="Sanctuary", occupancy=100)
		Room.objects.create(name="Charis", occupancy=1000)

		self.r1 = Room.objects.get(pk=1)
		self.r2 = Room.objects.get(pk=2)
		self.r3 = Room.objects.get(pk=3)


	def test_when_occupancy_is_empty(self):
		""" all rooms should be returned because occupancy should default
			to 0 when there is no value entered by the user """
		response = self.client.get(reverse('campus:search'))

		self.assertContains(response, self.r1.name)
		self.assertContains(response, self.r2.name)
		self.assertContains(response, self.r3.name)


	def test_when_all_rooms_have_a_higher_occupancy(self):
		""" all rooms should be returned because all rooms have an occupancy greater than 0 """
		response = self.client.get(reverse('campus:search'), {'occupancy': 0})

		self.assertContains(response, self.r1.name)
		self.assertContains(response, self.r2.name)
		self.assertContains(response, self.r3.name)


	def test_when_some_rooms_have_a_higher_occupancy(self):
		""" only rooms with a occupancy higher than 15 should be returned """
		response = self.client.get(reverse('campus:search'), {'occupancy': 15})

		self.assertNotContains(response, self.r1.name)
		self.assertContains(response, self.r2.name)
		self.assertContains(response, self.r3.name)


	def test_when_no_rooms_have_a_higher_occupancy(self):
		""" no rooms should be returned because the highest occupancy is 1000"""
		response = self.client.get(reverse('campus:search'), {'occupancy': 1500})

		self.assertNotContains(response, self.r1.name)
		self.assertNotContains(response, self.r2.name)
		self.assertNotContains(response, self.r3.name)



