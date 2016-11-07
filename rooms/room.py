import random
from os import sys, path

from sqlalchemy import Column, Integer, String

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from base import Base


class Room(Base):
    """Defines attributes and methods for the Room class"""
    __tablename__ = 'room'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    mem_id = Column(Integer)
    name = Column(String(50))
    floor = Column(Integer)
    no_of_occupants = Column(Integer, default=0)
    capacity = Column(Integer)
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'room'
    }

    @staticmethod
    def create_room(mem_id, name, floor, room_type, capacity,
                    no_of_occupants):
        """Create room object and return"""
        # I imported here to avoid cyclic imports
        import living_space
        import office
        if room_type == "office":
            new_room = office.Office(
                mem_id=mem_id, name=name, floor=floor,
                no_of_occupants=no_of_occupants,
                capacity=capacity["office"]
            )
        elif room_type == "living space":
            new_room = living_space.LivingSpace(
                mem_id=mem_id, name=name, floor=floor,
                no_of_occupants=no_of_occupants,
                capacity=capacity["living space"]
            )
        else:
            raise ValueError("Invalid Room Type!!! Room is either an "
                             "'office' or 'living space' not '{0}'."
                             .format(room_type))
        return new_room

    @staticmethod
    def is_room_type_valid(room_type):
        """Checks that the room type is either office or living space"""
        if room_type in ["office", "living space"]:
            return True
        else:
            return False

    def get_random_room(self, rooms, room_type):
        """
        Randomly pick an office or living space based on supplied argument
        Args:
            rooms -- all rooms in database
            room_type -- the room type of interest
        Returns:
            room -- a randomly selected room
        """
        index_list = range(len(rooms))
        random.shuffle(index_list)

        for index in index_list:
            if self.check_that_room_is_vacant(rooms[index], room_type):
                self.increment_number_of_occupants(rooms, index)
                return rooms[index]

    @staticmethod
    def check_that_room_is_vacant(room, room_type):
        """
        Returns true if this room is vacant and of a particular type
        Args:
            room -- the room to check
            room_type -- the room type of interest
        Returns:
            True -- if room is vacant
            False -- if room is full
        """
        return room.type == room_type and room.no_of_occupants < room.capacity

    @staticmethod
    def increment_number_of_occupants(rooms, room_index):
        """ Increases the number of occupants in room by one
        Args:
            room -- room to be updated
        Returns:
            updated room object
        """
        rooms[room_index].no_of_occupants += 1

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
        return False

    def remove_room_of_same_type(self, rooms, new_room, person):
        """
        Searches rooms that person belongs to so only old room
        of same type is removed in place of new room
        If no old room of the same type exists, a new one is allocated
        Args:
            rooms -- list of all rooms
            room -- room to allocate person
            person -- person to be allocated
        Returns:
            person object
        """
        for room in person.rooms:
            if room.type == new_room.type:
                person.rooms.remove(room)
                self.decrement_number_of_occupants(rooms, room.mem_id)
        return person

    @staticmethod
    def decrement_number_of_occupants(rooms, room_index):
        """Decreases number of occupants in room by one
        Args:
            room -- room to be updated
        Returns:
            updated room object
        """
        rooms[room_index].no_of_occupants -= 1

    def get_room(self, room_name, rooms):
        """
        Return room object that has the supllied room name
        if the room is vacant
        Args:
            room_name -- name of room that is to be returned
            rooms -- list of all rooms
        Returns:
            room -- a room object
            None -- if no room was found with that name
        """
        for counter, room in enumerate(rooms):
            if (self.check_that_room_is_vacant(room, room.type) and
                    room.name == room_name):
                return room
        return None

    @staticmethod
    def add_empty_rooms_to_allocation(rooms, allocations):
        """Returns all rooms that have no allocation
        Args:
            rooms -- list of all rooms
            allocations -- a dictionary mapping rooms to occupants
        Returns:
            allocations -- an updated dictionary containing empty rooms
        """
        copy_of_allocations = allocations
        for room in rooms:
            try:
                copy_of_allocations[room.name]
            except KeyError:
                copy_of_allocations[room.name] = ["Empty Room"]
        return copy_of_allocations

    def __str__(self):
        return "{0} {1}".format(self.name, self.type)
