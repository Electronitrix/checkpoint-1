import unittest
from context import persons, rooms, amity

class AmityRoomAllocationClassesTestSuite(unittest.TestCase):
    """Contains different test cases for the Amity Room Application classes."""

    def test_person_type(self):
        person = persons.person.Person(
                                  mem_id=0, 
                                  first_name="Erika", 
                                  last_name="Dike"
                               )
        self.assertTrue((type(person) is persons.person.Person), msg=
            "Person object was not Created!!!")

    def test_fellow_type(self):
        fellow = persons.fellow.Fellow(
                                  mem_id=0, 
                                  first_name="Erika", 
                                  last_name="Dike"
                               )
        self.assertTrue((type(fellow) is persons.fellow.Fellow), msg=
            "Fellow object was not Created!!!")

    def test_staff_type(self):
        staff = persons.staff.Staff(
                                mem_id=0, 
                                first_name="Erika", 
                                last_name="Dike"
                             )
        self.assertTrue((type(staff) is persons.staff.Staff), msg=
            "Staff object was not Created!!!")

    def test_room_type(self):
        room = rooms.room.Room(
                            name="Iroko", 
                            floor=1, 
                            no_of_occupants=0, 
                            capacity=0
                         )
        self.assertTrue((type(room) is rooms.room.Room), msg=
            "Room object was not Created!!!")

    def test_office_type(self):
        office = rooms.office.Office(
                                name="Bellows", 
                                floor=0, 
                                no_of_occupants=0, 
                                capacity=6
                             )
        self.assertTrue((type(office) is rooms.office.Office), msg=
            "Office object was not Created!!!")

    def test_living_space_type(self):
        living_space = rooms.living_space.LivingSpace(
                                           name="Iroko", 
                                           floor=1, 
                                           no_of_occupants=0, 
                                           capacity=0
                                        )
        self.assertTrue(
                          (type(living_space) is 
                          rooms.living_space.LivingSpace), 
                          msg="Fellow object was not Created!!!"
                       )

    def test_amity_object_initializes_correctly(self):
        app = amity.amity.Amity()
        self.assertListEqual(
            [6, 4, 0],
            [
                app.office_capacity,
                app.living_space_capacity,
                app.no_of_occupants
            ],
            msg="Amity object is not initialized with the right values"
        )