from __init__ import Room, LivingSpace, Office, Person, Fellow, Staff
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, func
import random

class Amity(object):
    """Defines the Amity class"""
    
    def __init__(self, office_capacity=6, living_space_capacity=4,
        no_of_occupants = 0):
        self.office_capacity = office_capacity
        self.living_space_capacity = living_space_capacity
        self.no_of_occupants = no_of_occupants
        
    def create_room(self, identifier, name, floor, room_type):
        """Create room object and return"""
        if room_type == "office":
            new_room = Office(
                                identifier=identifier, 
                                name=name, 
                                floor=floor,
                                no_of_occupants = self.no_of_occupants,
                                capacity=self.office_capacity
                             )
        else:
            new_room = LivingSpace(
                                    identifier=identifier, 
                                    name=name, 
                                    floor=floor,
                                    no_of_occupants = self.no_of_occupants,
                                    capacity=self.living_space_capacity
                                  )
        return new_room

    def create_person(self, identifier, first_name, last_name, employeeType, 
            wants_accommodation, rooms):
        """Create Person object"""
        if employeeType == "staff":
            new_person = Staff(identifier=identifier, first_name=first_name, 
                last_name=last_name)
        else:
            new_person = Fellow(identifier=identifier, first_name=first_name, 
                last_name=last_name)
        return self.randomly_allocate_rooms(
                                              new_person, 
                                              wants_accommodation,
                                              rooms
                                           )

    def randomly_allocate_rooms(self, person, wants_accommodation, rooms):
        """Allocate person to room
        Both staff and fellow are assigned office spaces
        Only fellow who indicates interest is assigned living space
        Args:
        person -- the person of interest
        wants_accommodation -- indicates if person wants accommodation or not
        rooms -- list of all created rooms
        Returns:
        a call to add_persons_to_room method 
        """
        allocated_space  = []
        if self.check_room_type_has_vacancy(rooms, "office"):
            allocated_space.append(self.randomly_pick_a_room(rooms, "office"))
        if person.type == "fellow" and wants_accommodation == "Y" \
            and self.check_room_type_has_vacancy(rooms, "living space"):
            allocated_space.append(self.randomly_pick_a_room(rooms, 
                                                             "living space"
                                                            ))
        return self.add_person_to_rooms(person, allocated_space)
        
    def check_room_type_has_vacancy(self, rooms, room_type):
        """
        Args:
        rooms -- all rooms in database
        room_type -- the room type of interest
        Returns:
        True -- if there is a vacant room of a particular type. 
        False -- if there is none
        """
        for room in rooms:
            if self.check_that_room_is_vacant(room, room_type):
                return True
        print "There is no vacant {0} currently in database!!!". \
            format(room_type.capitalize())
        return False

    def add_person_to_rooms(self, person, rooms):
        """Update Person rooms column with the new rooms assigned
        Args:
        person -- the person of interest
        rooms -- the rooms we want to allocate to person
        Returns:
        person -- the updated person object reflecting the allocation
        """
        for room in rooms:
            person.room.append(room)
            print "{0} {1} was assigned {2} {3}.".format(person.first_name, 
                person.last_name, room.name.capitalize(), room.type)
        return person

    def randomly_pick_a_room(self, rooms, room_type):
        """
        Randomly pick an office or living space based on supplied argument
        Args:
        rooms -- all rooms in database
        room_type -- the room type of interest
        Returns:
        room -- a randomly selected room
        """
        last_room_index = len(rooms) - 1
        random_index = random.randint(0, last_room_index)
        searching_for_vacant_room = True
        while searching_for_vacant_room:
            if self.check_that_room_is_vacant(rooms[random_index], room_type):
                self.increment_number_of_occupants(rooms, random_index)
                searching_for_vacant_room = False
            else:
                random_index = random.randint(0, last_room_index)
        return rooms[random_index]
            
    def increment_number_of_occupants(self, rooms, room_index):
        """ Increases the number of occupants in room by one
        Args:
        room -- room to be updated
        Returns:
        updated room object
        """
        rooms[room_index].no_of_occupants += 1

    def check_that_room_is_vacant(self, room, room_type):
        """
        Returns true if this room is vacant and of a particular type
        Args:
        room -- the room to check
        room_type -- the room type of interest
        Returns:
        True -- if room is vacant
        False -- if room is full
        """
        if room.type == room_type and room.no_of_occupants < room.capacity:
            return True
        else:
            return False

    def reallocate_person(self, person_identifier, room_name, people, rooms):
        """
        Transfer person with the supplied person identifier to a different room
        Also performs fresh allocations if person has not been allocated a room
        of this type.
        Args:
        person_identifier -- an identifier that recognizes person
        room_name -- name of new room
        people -- list of person objects
        rooms -- list of room objects
        Returns a list containing person
        """
        new_room = self.get_room(room_name, rooms)
        person = self.get_person(person_identifier, people)
        if not new_room:
            return []
        if not person:
            return []
        if person.type == "staff" and new_room.type == "living space":
            print "FAILURE!!! You cannot allocate 'living space' to staff"
            return []
        return self.search_persons_rooms_for_room_to_remove(
                                                             rooms, 
                                                             new_room, 
                                                             person
                                                           )
        
    def search_persons_rooms_for_room_to_remove(self, rooms, new_room, person):
        """
        Searches rooms that person belongs to so only old room
        of same type is removed in place of new room
        Args:
        rooms -- list of all rooms
        room -- room to allocate person
        person -- person to be allocated
        Returns:
        person object
        """
        for room_index in range(len(person.room)):
            if person.room[room_index].type == new_room.type:
                return self.exchange_old_room_for_new(rooms, new_room, room_index, 
                    person)
        return self.append_room_to_person(person, new_room, rooms)

    def exchange_old_room_for_new(self, rooms, new_room, room_index, person):
        """
        Replaces the old room for new
        Args:
        rooms -- list of all rooms
        new_room -- room to allocate person
        room_index -- position of new_
        Returns:
        person object
        """
        old_room_name = person.room.pop(room_index).name
        person.room.append(new_room)
        old_room = self.get_room(old_room_name, rooms)
        self.increment_number_of_occupants(rooms, old_room.identifier)
        self.decrement_number_of_occupants(rooms, new_room.identifier)
        print ("{0} Successfully moved from {1} to {2}".format \
                (person.first_name, old_room.name, new_room.name))
        return person

    def append_room_to_person(self, person, room, rooms):
        """
        Allocates room to person
        """
        self.add_person_to_rooms(person, [room])
        self.increment_number_of_occupants(rooms, room.identifier)
        print "{0} Successfully allocated {1} {2}".format \
            (person.first_name, room.name, room.type)
        return person

    def is_identifier_valid(self, person_identifier, people):
        "Checks if the person_identifier parameter passed in is valid"
        if person_identifier < len(people) and person_identifier >= 0:
            return True
        else:
            print "FAILURE!!! You entered an Invalid Identifier."
            return False

    def get_room(self, room_name, rooms):
        """
        Return room object that has the supllied room name
        if the room is vacant
        """
        for counter, room in enumerate(rooms):
            if self.check_that_room_is_vacant(room, room.type) and \
                room.name == room_name:
                return room
        print "FAILURE!!! The room you selected has no vacancy."
        return None

    def get_person(self, person_identifier, people):
        """
        Returns person object that has the supplied person identifier
        """
        for counter, person in enumerate(people):
            if person.identifier == person_identifier:
                return person
        print "FAILURE!!! You entered an Invalid Identifier."
        return None


    def decrement_number_of_occupants(self, rooms, room_index):
        """Decreases number of occupants in room by one
        Args:
        room -- room to be updated
        Returns:
        updated room object
        """
        rooms[room_index].no_of_occupants -= 1
        