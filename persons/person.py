from os import sys, path

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from base import Base
from allocation_table import allocation_table


class Person(Base):
    """Defines attributes and methods for the Person class"""
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    mem_id = Column(Integer)
    first_name = Column(String(20))
    last_name = Column(String(20))
    rooms = relationship(
        "Room", secondary=allocation_table, lazy='subquery'
    )
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'person'
    }

    def create_person(self, mem_id, first_name, last_name, employee_type):
        """Create fellow or staff object"""
        # I imported here to avoid cyclic imports
        import fellow
        import staff
        if employee_type == "staff":
            new_person = staff.Staff(mem_id=mem_id, first_name=first_name,
                                     last_name=last_name)
        elif employee_type == "fellow":
            new_person = fellow.Fellow(mem_id=mem_id, first_name=first_name,
                                       last_name=last_name)
        else:
            raise ValueError("Invalid Employee Type!!! Employee is either a "
                             "'fellow' or 'staff' not '{0}'."
                             .format(employee_type))
        return new_person

    def add_rooms_to_person(self, rooms):
        """Update Person rooms column with the new rooms assigned
        Args:
            person -- the person of interest
            rooms -- a list of rooms we want to allocate to person
        Returns:
            person -- the updated person object reflecting the allocation
        """
        for room in rooms:
            self.rooms.append(room)
        return self

    def get_person_id(self, first_name, last_name, people):
        """Return person's identifier"""
        for person in people:
            if (first_name == person.first_name and last_name ==
                    person.last_name):
                return person.mem_id

        raise ValueError("No identifier was found for the name supplied")

    def get_person(self, mem_id, people):
        """
        Looks for a person based on supplied id
        Args:
            mem_id -- person id
            people -- list of everyone in memory
        Returns
            person -- person object
            None -- if nothing is found
        """
        for counter, person in enumerate(people):
            if person.mem_id == mem_id:
                return person
        return None

    def get_allocations(self, people):
        """
        Return all allocations in memory
        Args:
            people -- list of all everyone in memory
        Returns:
            allocations -- a dictionary mapping rooms to people
        """
        allocations = {}
        for person in people:
            for room in person.rooms:
                key = room.name
                allocations[key] = allocations.get(key, []) + \
                    [person.first_name + " " + person.last_name]
        return allocations

    def get_unallocated(self, people, allocations):
        """
        Return all those who have not been allocated rooms
        """
        unallocated_people = []
        for person in people:
            found_match = False
            for key, value in allocations.iteritems():
                if ("{0} {1}".format(person.first_name, person.last_name) in
                        value):
                    found_match = True
            if not found_match:
                unallocated_people.append("{0} {1}".
                                          format(person.first_name.upper(),
                                                 person.last_name.upper()))
        return unallocated_people

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
