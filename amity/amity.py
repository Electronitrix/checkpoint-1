from __init__ import Room, LivingSpace, Office, Person, Fellow, Staff
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, func

class Amity(object):
    """Defines the Amity class"""
    
    office_capacity = 6
    living_space_capacity = 4
    initial_no_of_occupants = 0

    def create_room(self, name, floor, roomType):

        if roomType == "living space":
            new_room = LivingSpace(name=name, floor=floor, no_of_occupants=
                self.initial_no_of_occupants, capacity=self.living_space_capacity)
        else:
            new_room = Office(name=name, floor=floor, no_of_occupants=
                self.initial_no_of_occupants, capacity=self.office_capacity)
        return new_room

    def add_person(self, identifier, first_name, last_name, employeeType):
        if employeeType == "staff":
            new_person = Staff(identifier=identifier, first_name=first_name, 
                last_name=last_name)
        else:
            new_person = Fellow(identifier=identifier, first_name=first_name, 
                last_name=last_name)
        return new_person