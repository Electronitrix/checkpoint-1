from os import path, sys
import random

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# from persons.fellow import Fellow
from persons.person import Person
# from persons.staff import Staff
from rooms.living_space import LivingSpace 
from rooms.office import Office 
from rooms.room import Room


class Amity(object):
    """Defines the Amity class"""

    def __init__(self, office_capacity=6, living_space_capacity=4,
                 no_of_occupants=0):
        self.capacity = {"office": office_capacity,
                         "living space": living_space_capacity}
        self.no_of_occupants = no_of_occupants

    def create_room(self, mem_id, name, floor, room_type):
        """Create room object and return"""
        new_room = Room.create_room(
            mem_id, name, floor, room_type, self.capacity,
            self.no_of_occupants
        )
        return new_room

    @staticmethod
    def add_person(mem_id, first_name, last_name, employee_type,
                   wants_accommodation, rooms):
        """Adds new person to room
        Args:
            mem_id -- an id used to identify to objects held in memory
            first_name -- person's first name
            last_name -- person's last name
            employee_type -- is the person a fellow or staff
            wants_accommodation -- should be "Y" or "N" indicating if fellow
                                   wants accommodation
            rooms -- a list of all rooms in Amity
        Result:
            new_person -- a new Fellow or Staff object
            errors -- a list of non destructive errors that occurred
        """
        person = Person()
        room = Room()
        allocated_rooms = []
        errors = []
        new_person = person.create_person(
            mem_id, first_name, last_name, employee_type)

        if room.check_room_type_has_vacancy(rooms, "office"):
            allocated_rooms.append(room.get_random_room(rooms, "office"))
        else:
            errors.append("There is no vacant office currently in "
                          "Amity!!!")

        if new_person.type == "fellow" and wants_accommodation == "Y":
            if room.check_room_type_has_vacancy(rooms, "living space"):
                allocated_rooms.append(room.get_random_room(rooms,
                                       "living space"))
            else:
                errors.append("There is no vacant living space currently in "
                              "Amity!!!")

        new_person = new_person.add_rooms_to_person(allocated_rooms)
        return new_person, errors

    @staticmethod
    def is_room_type_valid(room_type):
        """Returns True if room type is valid and False, otherwise"""
        return Room.is_room_type_valid(room_type)

    @staticmethod
    def get_person_id(first_name, last_name, people):
        """Searches for person identifier
        Returns:
        Person's identifier or failure message
        """
        return Person.get_person_id(first_name, last_name, people)

    @staticmethod
    def reallocate_person(person_id, room_name, people, rooms):
        """
        Transfer person with the supplied person identifier to a different room
        Also performs fresh allocations if person has not been allocated a room
        of this type.
        Args:
            person_identifier -- an identifier that recognizes person
            room_name -- name of new room
            people -- list of person objects
            rooms -- list of room objects
        Returns
            aperson -- person object with updates to the rooms attribute
            errors -- a list of non destructive errors that occurred
        """
        person = Person()
        room = Room()
        new_room = room.get_room(room_name, rooms)
        person = person.get_person(person_id, people)
        if not new_room:
            raise ValueError("No room was found in memory with that name. "
                             "You may want to create a new room with that\n"
                             "name or view all rooms in memory by requesting "
                             "allocations.")
        if not person:
            raise ValueError("No person was found in memory for person "
                             "identifier supplied.")
        if person.type == "staff" and new_room.type == "living space":
            raise RuntimeError("You cannot allocate staff to 'living space'.")
        person = room.remove_room_of_same_type(rooms, new_room, person)
        person.add_rooms_to_person([new_room])
        room.increment_number_of_occupants(rooms, new_room.mem_id)
        return person

    @staticmethod
    def get_allocations_as_dict(people, rooms=None):
        """Get allocation table from pkl file and return as dictionary"""
        if rooms is None:
            rooms = []
        allocations = Person.get_allocations(people)
        allocations = Room.add_empty_rooms_to_allocation(rooms, allocations)
        return allocations

    def get_unallocated_people(self, people):
        """
        Searches memory for all persons that have not been assigned
        a room.
        """
        allocations = self.get_allocations_as_dict(people)
        return Person.get_unallocated(people, allocations)
