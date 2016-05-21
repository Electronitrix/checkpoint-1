import os
import textwrap
import unittest

from context_manager import capture
from .context import main


class AmityRoomAllocationFunctionalityTestSuite(unittest.TestCase):
    """
    Contains different test cases for the Amity Room Application functins.
    """

    def setUp(self):
        self.rooms_file = "rooms.pkl"
        self.people_file = "people.pkl"
        self.people_txt_file = "people.txt"
        self.alloc_txt_file = "alloc.txt"
        self.unalloc_txt_file = "unalloc.txt"

    def test_create_room(self):
        main.create_room("Iroko", 1, "living space")
        rooms = main.get_list_of_objects(self.rooms_file)
        self.assertListEqual(
            ["iroko", 1, 0, 4, "living space"],
            [
                rooms[0].name,
                rooms[0].floor,
                rooms[0].no_of_occupants,
                rooms[0].capacity,
                rooms[0].type
            ],
            msg=("create_room function does not initialize Room with the "
                 "right values!!!")
        )

    def test_add_person(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        people = main.get_list_of_objects(self.people_file)
        self.assertListEqual(
            ["erika", "dike", "staff"],
            [
                people[0].first_name,
                people[0].last_name,
                people[0].type
            ],
            msg=("add_person function does not initialize Person object with "
                 "the right values")
        )

    def test_allocate_staff(self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        people = main.get_list_of_objects(self.people_file)
        self.assertListEqual(
            ["bellows", 1, "office"],
            [
                people[0].rooms[0].name,
                people[0].rooms[0].no_of_occupants,
                people[0].rooms[0].type
            ],
            msg=("add_person function should randomly allocate staff to an "
                 "office space")
        )

    def test_allocate_fellow(self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        people = main.get_list_of_objects(self.people_file)
        self.assertListEqual(
            ["bellows", 1, "office", "iroko", 1, "living space"],
            [
                people[0].rooms[0].name,
                people[0].rooms[0].no_of_occupants,
                people[0].rooms[0].type,
                people[0].rooms[1].name,
                people[0].rooms[1].no_of_occupants,
                people[0].rooms[1].type
            ],
            msg=("add_person function should randomly allocate fellow both "
                 "office and living space if fellow wants living space")
        )

    def test_allocate_fellow_when_fellow_does_not_want_accommodation(self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow")
        people = main.get_list_of_objects(self.people_file)
        self.assertEqual(
            1, len(people[0].rooms),
            msg=("add_person function should randomly allocate fellow only "
                 "office space if fellow does want living space")
        )

    def test_fellow_allocated_office_when_fellow_does_not_want_accommodation(
            self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow")
        people = main.get_list_of_objects(self.people_file)
        self.assertEqual(
            "office", people[0].rooms[0].type,
            msg=("add_person function should randomly allocate fellow only "
                 "office space if fellow does want living space")
        )

    def test_that_person_is_not_allocated_filled_office_space(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        main.add_person("sunday", "nwuguru", "staff")
        main.add_person("stephen", "oduntan", "staff")
        main.add_person("seyi", "adekoya", "staff")
        main.add_person("rikky", "dyke", "staff")
        main.add_person("eze", "janu", "staff")
        main.add_person("nwa", "kanwa", "staff")
        people = main.get_list_of_objects(self.people_file)
        self.assertEqual(
            [], people[6].rooms,
            msg=("An office space should not take more than 6 people!!! It "
                 "takes {0}").format(people[6].rooms)
        )

    def test_that_staff_not_allocated_living_space_even_if_wants(self):
        main.create_room("iroko", 1, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff", "Y")
        people = main.get_list_of_objects(self.people_file)
        self.assertEqual(
            1, len(people[0].rooms),
            msg="Staff cannot be allocated a living space!!!"
        )

    def test_print_person_identifier(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        test_output = ("ERIKA DIKE's identifier: 0\n")
        with capture(main.print_person_id, "erika", "dike") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("get_person_identifier does not print as expected!!! "
                     "{0} != {1}").format(test_output, app_output)
            )

    def test_print_invalid_person_identifier(self):
        main.add_person("erika", "dike", "staff")
        test_output = ("No identifier was found for the name supplied\n")
        with capture(main.print_person_id, "ina", "dike") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("{0} != {1}").format(test_output, app_output)
            )

    def test_graceful_handling_when_adding_person_and_no_room_exists(self):
        main.add_person("erika", "dike", "staff")
        people = main.get_list_of_objects(self.people_file)
        self.assertEqual(
            [], people[0].rooms,
            msg=("The room field of Person object should be an empty list "
                 "when no rooms have been created!!!")
        )

    def test_reallocate_person_moves_person_to_new_room(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        main.create_room("bench hook", 0, "office")
        main.reallocate_person(0, "bench hook")
        people = main.get_list_of_objects(self.people_file)
        self.assertEqual(
            "bench hook", people[0].rooms[0].name,
            msg="Person was not reallocated!!!"
        )

    def test_that_reallocate_person_allocates_person_without_room(self):
        main.add_person("erika", "dike", "staff")
        main.create_room("bellows", 0, "office")
        main.reallocate_person(0, "bellows")
        people = main.get_list_of_objects(self.people_file)
        self.assertEqual("bellows", people[0].rooms[0].name,
                         msg="Person was not reallocated!!!")

    def test_cannot_reallocate_staff_to_living_space(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        main.create_room("iroko", 1, "living space")
        test_output = "You cannot allocate staff to 'living space'.\n"
        with capture(main.reallocate_person, 0, "iroko") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("Staff cannot be reallocated to living space!!! {0} != "
                     "{1}".format(test_output, app_output))
            )

    def test_invalid_person_identifiers_arguments_to_reallocate_person(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "staff")
        main.create_room("bench hook", 0, "office")
        test_output = ("No person was found in memory for person identifier "
                       "supplied.\n")
        with capture(main.reallocate_person, 45, "bench hook") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg="{0} != {1}".format(test_output, app_output)
            )

    def test_does_not_allocate_to_filled_living_space(self):
        main.create_room("iroko", 1, "living space")
        main.add_person("erika", "dike", "fellow", "Y")
        main.add_person("eze", "janu", "fellow", "Y")
        main.add_person("sunday", "nwuguru", "fellow", "Y")
        main.add_person("stephen", "oduntan", "fellow", "Y")
        main.add_person("seyi", "adekoya", "fellow", "Y")
        test_output = ("No room was found in memory with that name. You may "
                       "want to create a new room with that\n"
                       "name or view all rooms in memory by requesting "
                       "allocations.\n"
                       )
        with capture(main.reallocate_person, 4, "iroko") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("{0} != {1}".format(test_output, app_output))
            )

    def test_loads_people(self):
        input_file = ("erika dike FELLOW Y\n"
                      "eze janu FELLOW Y\n"
                      "stephen oduntan FELLOW\n"
                      "NENGI ADOKI STAFF N\n"
                      )
        with open(self.people_txt_file, 'w') as file:
            file.write(input_file)
        main.loads_people(self.people_txt_file)
        people = main.get_list_of_objects(self.people_file)
        self.assertListEqual(
            [
                ["erika", "dike", "fellow"],
                ["eze", "janu", "fellow"],
                ["stephen", "oduntan", "fellow"],
                ["nengi", "adoki", "staff"]
            ],
            [
                [people[0].first_name, people[0].last_name, people[0].type],
                [people[1].first_name, people[1].last_name, people[1].type],
                [people[2].first_name, people[2].last_name, people[2].type],
                [people[3].first_name, people[3].last_name, people[3].type]
            ],
            msg=("loads_people does not load correctly")
        )

    def test_print_allocations_when_there_are_allocations(self):
        self.add_data_to_memory_for_print_allocation_tests()
        test_output = self.prepare_test_output()
        test_output += "\n"
        with capture(main.print_allocations, "screen") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("{0} != {1}!!!".format(test_output, app_output))
            )

    def test_print_allocations_to_file(self):
        self.add_data_to_memory_for_print_allocation_tests()
        main.print_allocations(self.alloc_txt_file)
        with open(self.alloc_txt_file, "r") as file:
            allocations = file.read()

        test_output = self.prepare_test_output()

        self.assertEqual(
            test_output, allocations,
            msg=("{0} != {1}!!!".format(test_output, allocations))
        )

    @staticmethod
    def add_data_to_memory_for_print_allocation_tests():
        main.create_room("iroko", 0, "living space")
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        main.add_person("eze", "janu", "fellow", "Y")
        main.add_person("sunday", "nwuguru", "fellow", "Y")
        main.add_person("stephen", "oduntan", "fellow", "Y")
        main.add_person("nengi", "adoki", "staff")

    @staticmethod
    def prepare_test_output():
        app_output = []
        temp = []
        line_width = 51

        temp.append("BELLOWS\n")
        temp.append("-" * line_width)
        temp.append("\nERIKA DIKE, EZE JANU, SUNDAY NWUGURU, ")
        temp.append("STEPHEN ODUNTAN, NENGI ADOKI")
        app_output.append(textwrap.fill("".join(temp), line_width))
        app_output.append("\n\n")

        temp = []
        temp.append("IROKO\n")
        temp.append("-" * line_width)
        temp.append("\nERIKA DIKE, EZE JANU, SUNDAY NWUGURU, "
                    "STEPHEN ODUNTAN\n\n\n")
        app_output.append(textwrap.fill("".join(temp), line_width))
        app_output.append("\n\n")
        return "".join(app_output)

    def test_print_allocations_when_there_are_no_allocations(self):
        test_output = ("There are no allocations in memory. You can either "
                       "enter new data or load data from database\n")
        with capture(main.print_allocations, "screen") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("- {0} != {1}!!!".format(test_output, app_output))
            )

    def test_print_allocations_invalid_file(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        test_output = ("You must enter a file name with a .txt extension to "
                       "save to file\n")
        with capture(main.print_allocations, "alloc.pkl") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("print_allocations does not detect invalid file "
                     "extensions - {0} != {1}".format(test_output, app_output))
            )

    def test_print_unallocated(self):
        main.add_person("erika", "dike", "fellow", "Y")
        test_output = ("LIST OF ALL UNALLOCATED PEOPLE\n\n"
                       "ERIKA DIKE\n\n")
        with capture(main.print_unallocated, "screen") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("{0} != {1}!!!".format(test_output, app_output))
            )

    def test_print_unallocated_to_file(self):
        main.add_person("erika", "dike", "fellow", "Y")
        main.print_unallocated(self.unalloc_txt_file)

        with open(self.unalloc_txt_file, "r") as file:
            unallocated = file.read()

        test_output = ("LIST OF ALL UNALLOCATED PEOPLE\n\nERIKA DIKE\n")
        self.assertEqual(
            test_output, unallocated,
            msg=("{0} != {1}".format(test_output, unallocated))
        )

    def test_print_unallocated_invalid_file(self):
        main.add_person("erika", "dike", "fellow", "Y")
        test_output = ("You must enter a file name with a .txt extension to "
                       "save to file\n")

        with capture(main.print_unallocated, "unalloc.pkl") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("{0} != {1}".format(test_output, app_output))
            )

    def test_print_room_with_occupants(self):
        main.create_room("bellows", 0, "office")
        main.add_person("erika", "dike", "fellow", "Y")
        test_output = ("NAMES OF PEOPLE IN BELLOWS\n\nERIKA DIKE\n\n\n")

        with capture(main.print_room, "bellows") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("print_room does not print correct room content "
                     "- {0} != {1}!!!".format(test_output, app_output))
            )

    def test_print_room_with_out_occupants(self):
        main.create_room("bellows", 0, "office")
        test_output = ("NAMES OF PEOPLE IN BELLOWS\n\n"
                       "There is no one in this Room!!!\n\n"
                       )
        with capture(main.print_room, "bellows") as app_output:
            self.assertEqual(
                test_output, app_output,
                msg=("print_room does not print correct room content "
                     "- {0} != {1}!!!".format(test_output, app_output))
            )

    def tearDown(self):
        if os.path.isfile(self.rooms_file):
            os.remove(self.rooms_file)
        if os.path.isfile(self.people_file):
            os.remove(self.people_file)
        if os.path.isfile(self.alloc_txt_file):
            os.remove(self.alloc_txt_file)
        if os.path.isfile(self.unalloc_txt_file):
            os.remove(self.unalloc_txt_file)
