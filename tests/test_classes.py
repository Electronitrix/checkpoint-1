import unittest
from context import persons, rooms, amity

class AmityRoomAllocationClassesTestSuite(unittest.TestCase):
    """Contains different test cases for the Amity Room Application classes."""

    def setUp(self):
        self.amity = amity.Amity()

    def test_person_type(self):
        person = persons.Person(
                                  identifier=0, 
                                  first_name="Erika", 
                                  last_name="Dike"
                               )
        self.assertTrue((type(person) is persons.Person), msg=
            "Person object was not Created!!!")

    def test_fellow_type(self):
        fellow = persons.Fellow(
                                  identifier=0, 
                                  first_name="Erika", 
                                  last_name="Dike"
                               )
        self.assertTrue((type(fellow) is persons.Fellow), msg=
            "Fellow object was not Created!!!")

    def test_staff_type(self):
        staff = persons.Staff(
                                identifier=0, 
                                first_name="Erika", 
                                last_name="Dike"
                             )
        self.assertTrue((type(staff) is persons.Staff), msg=
            "Staff object was not Created!!!")

    def test_room_type(self):
        room = rooms.Room(
                            name="Iroko", 
                            floor=1, 
                            no_of_occupants=0, 
                            capacity=0
                         )
        self.assertTrue((type(room) is rooms.Room), msg=
            "Room object was not Created!!!")

    def test_office_type(self):
        office = rooms.Office(
                                name="Bellows", 
                                floor=0, 
                                no_of_occupants=0, 
                                capacity=6
                             )
        self.assertTrue((type(office) is rooms.Office), msg=
            "Office object was not Created!!!")

    def test_living_space_type(self):
        living_space = rooms.LivingSpace(
                                           name="Iroko", 
                                           floor=1, 
                                           no_of_occupants=0, 
                                           capacity=0
                                        )
        self.assertTrue(
                          (type(living_space) is 
                          rooms.LivingSpace), 
                          msg="Fellow object was not Created!!!"
                       )

    def test_amity_object_initializes_correctly(self):
        self.assertListEqual(
            [6, 4, 0],
            [
                self.amity.office_capacity,
                self.amity.living_space_capacity,
                self.amity.no_of_occupants
            ],
            msg="Amity object is not initialized with the right values"
        )