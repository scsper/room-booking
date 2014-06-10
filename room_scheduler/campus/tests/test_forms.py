from django.test import TestCase

from campus.models import Room, Attribute

# from campus.forms import RoomSearchForm


class RoomSearchFormTest(TestCase):
    def setUp(self):
        self.r1 = Room.objects.create(name='room1', occupancy=10)
        self.r2 = Room.objects.create(name='room2', occupancy=50)
        self.r3 = Room.objects.create(name='room3', occupancy=75)

        self.a1 = Attribute.objects.create(name="attr1")
        self.a2 = Attribute.objects.create(name="attr2")
        self.a3 = Attribute.objects.create(name="attr3")
        self.a4 = Attribute.objects.create(name="attr4")


        self.r1.attributes.add(self.a1, self.a2)
        self.r2.attributes.add(self.a2, self.a3)
        self.r3.attributes.add(self.a3)


    def test_search_with_occupancy_below_available(self):
        """test the search returns all rooms"""
        from campus.forms import RoomSearchForm
        rooms = RoomSearchForm().search(0, [])
        self.assertEquals(rooms[0].name, "room1")
        self.assertEquals(rooms[1].name, "room2")
        self.assertEquals(rooms[2].name, "room3")

    def test_search_with_occupancy_in_middle(self):
        from campus.forms import RoomSearchForm
        rooms = RoomSearchForm().search(20, [])
        self.assertEquals(len(rooms), 2)
        self.assertEquals(rooms[0].name, "room2")
        self.assertEquals(rooms[1].name, "room3")

    def test_search_with_occupancy_greater_than_available(self):
        from campus.forms import RoomSearchForm
        rooms = RoomSearchForm().search(100, [])
        self.assertEquals(len(rooms), 0)

    def test_search_with_occupancy_and_attributes(self):
        from campus.forms import RoomSearchForm
        attrs = Attribute.objects.all()

        rooms = RoomSearchForm().search(40, [self.a2])
        self.assertEquals(len(rooms), 1)
        self.assertEquals(rooms[0].name, "room2")

    # def test_search_by_nothing(self):
    #    	form = RoomSearchForm({})
    	
    # def test_search_by_empty_attribute_tag(self):
    # def test_search_by_empty_occupancy_tag(self):
    # def test_search_by_empty_attribute_and_occupancy_tags(self):

    # def test_search_by_one_attr_get_none(self):
    # def test_search_by_one_attr_get_one(self):
    # def test_search_by_one_attr_get_many(self):
    # def test_search_by_many_attrs_get_none(self):
    # def test_search_by_many_attrs_get_one(self):
    # def test_search_by_many_attrs_get_many(self):

    # def test_search_by_occupancy_all_higher(self):
    # def test_search_by_occupancy_some_higher(self):
    # def test_search_by_occupancy_none_higher(self):

