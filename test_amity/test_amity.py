import unittest, os, sys, inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
currentdir = os.path.dirname(os.path.abspath(inspect. \
    getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from amity import base
from amity import main
from amity.amity import Amity
from amity.persons.person import Person
from amity.persons.fellow import Fellow
from amity.persons.staff import Staff
from amity.rooms.room import Room
from amity.rooms.office import Office
from amity.rooms.living_space import LivingSpace
from context_manager import capture

class AmityRoomAllocationClassesTestSuite(unittest.TestCase):
    """Contains different test cases for the Amity Room Application classes."""

    def setUp(self):
        self.amity = Amity()

    def test_person_type(self):
        person = Person(identifier=0, firstName="Erika", lastName="Dike")
        self.assertTrue((type(person) is Person), msg=
            "Person object was not Created!!!")

    def test_fellow_type(self):
        fellow = Fellow(identifier=0, firstName="Erika", lastName="Dike")
        self.assertTrue((type(fellow) is Fellow), msg=
            "Fellow object was not Created!!!")

    def test_staff_type(self):
        staff = Staff(identifier=0, firstName="Erika", lastName="Dike")
        self.assertTrue((type(staff) is Staff), msg=
            "Staff object was not Created!!!")

    def test_room_type(self):
        room = Room(name="Iroko", floor=1, noOfOccupants=0, capacity=0)
        self.assertTrue((type(room) is Room), msg=
            "Room object was not Created!!!")

    def test_office_type(self):
        office = Office(name="Bellows", floor=0, noOfOccupants=0, capacity=6)
        self.assertTrue((type(office) is Office), msg=
            "Office object was not Created!!!")

    def test_living_space_type(self):
        living_space = LivingSpace(name="Iroko", floor=1, noOfOccupants=0, capacity=0)
        self.assertTrue((type(living_space) is LivingSpace), msg=
            "Fellow object was not Created!!!")

    def test_amity_object_initializes_correctly(self):
        self.assertListEqual(
            [6, 4, 0],
            [
                self.amity.officeCapacity,
                self.amity.livingSpaceCapacity,
                self.amity.initialNoOfOccupants
            ],
            msg="Amity object is not initialized with the right values"
        )

class AmityRoomAllocationFunctionalityTestSuite(unittest.TestCase):
    """Contains different test cases for the Amity Room Application functins."""

    def setUp(self):
        self.amity = Amity()

    def test_create_room(self):
        main.create_room("Iroko", 1, "living space")
        room_objects = main.get_rooms_as_list()
        self.assertListEqual(
            ["iroko", 1, 0, 4, "living space"],
            [
                room_objects[0].name,
                room_objects[0].floor,
                room_objects[0].noOfOccupants,
                room_objects[0].capacity,
                room_objects[0].type
            ],
            msg=("create_room function does not initialize Room with the "
                 "right values!!!")
        )
        os.remove("rooms.pkl")

    def test_add_person(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        person_objects = main.get_persons_as_list()
        self.assertListEqual(
            ["erika", "dike", "staff"],
            [
                person_objects[0].firstName,
                person_objects[0].lastName,
                person_objects[0].type
            ],
            msg=("add_person function does not initialize Person object with "
                 "the right values")
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

    def test_allocate_staff(self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        person_objects = main.get_persons_as_list()
        self.assertListEqual(
            ["bellows", 1, "office"],
            [
                person_objects[0].room[0].name,
                person_objects[0].room[0].noOfOccupants,
                person_objects[0].room[0].type
            ],
            msg=("add_person function should randomly allocate staff to an "
                 "office space")
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")        

    def test_allocate_fellow(self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        person_objects = main.get_persons_as_list()
        #import pdb
        #pdb.set_trace()
        self.assertListEqual(
            ["bellows", 1, "office", "iroko", 1, "living space"],
            [
                person_objects[0].room[0].name,
                person_objects[0].room[0].noOfOccupants,
                person_objects[0].room[0].type,
                person_objects[0].room[1].name,
                person_objects[0].room[1].noOfOccupants,
                person_objects[0].room[1].type
            ],
            msg=("add_person function should randomly allocate fellow both "
                 "office and living space if fellow wants living space")
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")        

    def test_allocate_fellow_when_fellow_does_not_want_accommodation(self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow")
        person_objects = main.get_persons_as_list()
        self.assertEqual(1, len(person_objects[0].room),
            msg=("add_person function should randomly allocate fellow only "
                 "office space if fellow does want living space")
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")        

    def test_fellow_allocated_office_when_fellow_does_not_want_accommodation \
        (self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow")
        person_objects = main.get_persons_as_list()
        self.assertEqual("office", person_objects[0].room[0].type,
            msg=("add_person function should randomly allocate fellow only "
                 "office space if fellow does want living space")
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

    def test_that_person_is_not_allocated_filled_office_space(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        main.add_person("sunday", "nwuguru", "staff")
        main.add_person("stephen", "oduntan", "staff")
        main.add_person("seyi", "adekoya", "staff")
        main.add_person("rikky", "dyke", "staff")
        main.add_person("eze", "janu", "staff")
        main.add_person("nwa", "kanwa", "staff")
        person_objects = main.get_persons_as_list()
        self.assertEqual([], person_objects[6].room,
            msg="An office space should not take more than 6 people!!! It takes {0}".format(person_objects[6].room)
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

    def test_that_staff_not_allocated_living_space_even_if_wants(self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff", "Y")
        person_objects = main.get_persons_as_list()
        self.assertEqual(1, len(person_objects[0].room),
            msg="Staff cannot be allocated a living space!!!"
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

    def test_get_person_identifier(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        appOutput = ("ERIKA DIKE's identifier: 0\n")
        with capture(main.get_person_identifier, "erika", "dike") as output:
            self.assertEqual(appOutput, output,
                msg="get_person_identifier does not print as expected!!! {0} != {1}".format(appOutput, output)
            )
        
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

    def test_graceful_handling_when_adding_person_and_no_room_exists(self):
        main.add_person("erika", "dike", "staff")
        person_objects = main.get_persons_as_list()
        self.assertEqual([], person_objects[0].room,
            msg=("The room field of Person object should be an empty list "
                 "when no rooms have been created!!!")
        )
        os.remove("persons.pkl")

    def test_reallocate_person_moves_person_to_new_room(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        main.create_room("bench hook", 0, "office")
        main.reallocate_person(0, "bench hook")
        person_objects = main.get_persons_as_list()
        self.assertEqual("bench hook", person_objects[0].room[0].name,
            msg="Person is not reallocated!!!"
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

        
    def test_cannot_reallocate_staff_to_living_space(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        main.create_room("iroko", 1, "living space")
        appOutput = "FAILURE!!! You cannot allocate 'living space' to staff\n"
        with capture(main.reallocate_person, 0, "iroko") as output:
            self.assertEqual(appOutput, output,
                msg="Staff cannot be reallocated to living space!!! {0} != {1}".format(appOutput, output)
            )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

    def test_invalid_person_idenfiers_arguments_to_reallocate_person(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        main.create_room("bench hook", 0, "office")
        appOutput = "FAILURE!!! You entered an Invalid Identifier.\n"
        with capture(main.reallocate_person, 45, "bench hook") as output:
            self.assertEqual(appOutput, output,
                msg="reallocate_person does not detect invalid identifiers!!!"
            )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

    def test_does_not_allocate_to_filled_office(self):
        main.create_room("iroko", 0, "living space")
        main.add_person("erika", "dike", "fellow", "Y")
        main.add_person("eze", "janu", "fellow", "Y")
        main.add_person("sunday", "nwuguru", "fellow", "Y")
        main.add_person("stephen", "oduntan", "fellow", "Y")
        main.add_person("seyi", "adekoya", "fellow", "Y")
        appOutput = "FAILURE!!! The room you selected has no vacancy.\n"
        with capture(main.reallocate_person, 4, "iroko") as output:
            self.assertEqual(appOutput, output,
                msg=("reallocate_person allocates person to filled living "
                     "space!!! {0} != {1}".format(appOutput, output))
            )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")

    def test_loads_people(self):
        input_file = ("erika dike FELLOW Y\n"
                      "eze janu FELLOW Y\n"
                      "stephen oduntan FELLOW\n"
                      "NENGI ADOKI STAFF N\n"
                     )
        with open("people.txt", 'w') as file:
            file.write(input_file)
        main.loads_people("people.txt")
        person_objects = main.get_persons_as_list()
        self.assertListEqual(
            [
                ["erika", "dike", "fellow"],
                ["eze", "janu", "fellow"],
                ["stephen", "oduntan", "fellow"],
                ["nengi", "adoki", "staff"]
            ],
            [
                [person_objects[0].firstName, person_objects[0].lastName, \
                    person_objects[0].type],
                [person_objects[1].firstName, person_objects[1].lastName, \
                    person_objects[1].type],
                [person_objects[2].firstName, person_objects[2].lastName, \
                    person_objects[2].type],
                [person_objects[3].firstName, person_objects[3].lastName, \
                    person_objects[3].type]    
            ],
            msg=("loads_people does not load correctly")
        )
        os.remove("persons.pkl")
        os.remove("people.txt")

    def test_print_allocations_when_there_are_allocations(self):
        main.create_room("iroko", 0, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        main.add_person("eze", "janu", "fellow", "Y")
        main.add_person("sunday", "nwuguru", "fellow", "Y")
        main.add_person("stephen", "oduntan", "fellow", "Y")
        main.add_person("nengi", "adoki", "staff")
        appOutput = ("BELLOWS\n"
                     "-------------------------------------------\n"
                     "ERIKA DIKE, EZE JANU, SUNDAY NWUGURU, STEPHEN ODUNTAN, "
                     "NENGI ADOKI\n\n"
                     "IROKO\n"
                     "-------------------------------------------\n"
                     "ERIKA DIKE, EZE JANU, SUNDAY NWUGURU, STEPHEN ODUNTAN"
                     "\n\n\n"
                    )
        with capture(main.print_allocations, "screen") as output:
            self.assertEqual(appOutput, output,
                msg=("print_allocations does not print as expected "
                     "- {0} != {1}!!!".format(appOutput, output))
            )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")    

    def test_print_allocations_when_there_are_no_allocations(self):
        appOutput = "There are no allocations in database\n"
        with capture(main.print_allocations, "screen") as output:
            self.assertEqual(appOutput, output,
                msg=("print_allocations does not print as expected "
                     "- {0} != {1}!!!".format(appOutput, output))
            )
        
    def test_print_allocations_to_file(self):
        main.create_room("iroko", 0, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        main.add_person("eze", "janu", "fellow", "Y")
        main.add_person("sunday", "nwuguru", "fellow", "Y")
        main.add_person("stephen", "oduntan", "fellow", "Y")
        main.add_person("nengi", "adoki", "staff")
        main.print_allocations("alloc.txt")
        with open("alloc.txt", "r") as file:
            allocations = file.read()
        appOutput = ("BELLOWS\n"
                     "-------------------------------------------\n"
                     "ERIKA DIKE, EZE JANU, SUNDAY NWUGURU, STEPHEN ODUNTAN, "
                     "NENGI ADOKI\n\n"
                     "IROKO\n"
                     "-------------------------------------------\n"
                     "ERIKA DIKE, EZE JANU, SUNDAY NWUGURU, STEPHEN ODUNTAN"
                     "\n\n"
                    )
        self.assertEqual(appOutput, allocations,
            msg=("print_allocations does not print proper values to file. "
                 "{0} != {1}!!!".format(appOutput, allocations))
        )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")
        os.remove("alloc.txt")

    def test_print_allocations_invalid_file(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        appOutput = ("You must enter a file name with a .txt extension to save"
                     " to file\n")
        with capture(main.print_allocations, "alloc.pkl") as output:
            self.assertEqual(appOutput, output,
                msg=("print_allocations does not detect invalid file "
                     "extensions - {0} != {1}".format(appOutput, output))
            )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")
        
    def test_print_unallocated(self):
        main.add_person("erika", "dike", "fellow", "Y")
        appOutput = ("LIST OF ALL UNALLOCATED PEOPLE\n\n"
                     "ERIKA DIKE\n\n")
        with capture(main.print_unallocated, "screen") as output:
            self.assertEqual(appOutput, output,
                msg=("print_unallocated does not print as expected "
                     "- {0} != {1}!!!".format(appOutput, output))
            )
        os.remove("persons.pkl")
        
    def test_print_unallocated_to_file(self):
        main.add_person("erika", "dike", "fellow", "Y")
        main.print_unallocated("unalloc.txt")
        with open("unalloc.txt", "r") as file:
            unallocated = file.read()
        appOutput = ("LIST OF ALL UNALLOCATED PEOPLE\n\n"
                     "ERIKA DIKE\n")
        self.assertEqual(appOutput, unallocated,
            msg=("print_unallocated does not print as expected to file - "
                 "{0} != {1}".format(appOutput, unallocated))
        )
        os.remove("persons.pkl")
        os.remove("unalloc.txt")
    
    def test_print_unallocated_invalid_file(self):
        main.add_person("erika", "dike", "fellow", "Y")
        appOutput = ("You must enter a file name with a .txt extension to save"
                     " to file\n")
        with capture(main.print_unallocated, "unalloc.pkl") as output:
            self.assertEqual(appOutput, output,
                msg=("print_unallocated does not detect invalid file "
                     "extensions - {0} != {1}".format(appOutput, output))
            )
        os.remove("persons.pkl")

    def test_print_room_with_occupants(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        appOutput = ("NAMES OF PEOPLE IN BELLOWS\n\n"
                     "ERIKA DIKE\n\n\n"
                    )
        with capture(main.print_room, "bellows") as output:
            self.assertEqual(appOutput, output,
                msg=("print_room does not print correct room content "
                     "- {0} != {1}!!!".format(appOutput, output))
            )
        os.remove("rooms.pkl")
        os.remove("persons.pkl")    

    def test_print_room_with_out_occupants(self):
        main.create_room("bellows", 0, "office")
        appOutput = ("NAMES OF PEOPLE IN BELLOWS\n\n"
                     "There is no one in this Room!!!\n\n"
                    )
        with capture(main.print_room, "bellows") as output:
            self.assertEqual(appOutput, output,
                msg=("print_room does not print correct room content "
                     "- {0} != {1}!!!".format(appOutput, output))
            )
        os.remove("rooms.pkl")
            
    # def test_save_state(self):
    #     # set up database
    #     import pdb
    #     pdb.set_trace()
    #     engine = create_engine("sqlite:///test.db")
    #     base.Base.metadata.create_all(engine, checkfirst=True)
    #     Session = sessionmaker(bind=engine)
    #     session = Session()
    #     # add data to application
    #     main.create_room("bellows", 0, "office")
    #     main.add_person("erika", "dike", "fellow", "Y")
    #     # save state
    #     main.save_state("test.db")
    #     # query DB
    #     person_objects = session.query(Person).all()
    #     room_objects = session.query(Room).all()
    #     self.assertListEqual(
    #         [
    #             ["erika", "dike", "fellow"],
    #             ["bellows", 0, "office"]
    #         ],
    #         [
    #             [person_objects[0].firstName, person_objects[0].lastName, \
    #                 person_objects[0].type],
    #             [room_objects[0].name, room_objects[0].floor, \
    #                 room_objects[0].type]
    #         ],
    #         msg=("save_state does not save appropriately!!!")
    #     )
    #     os.remove("rooms.pkl")
    #     os.remove("persons.pkl")
    #     os.remove("test.db")



if __name__ == "__main__":
    unittest.main()