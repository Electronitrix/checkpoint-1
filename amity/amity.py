from __init__ import Room, LivingSpace, Office, Person, Fellow, Staff
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, func

class Amity(object):
    """Defines the Amity class"""
    
    officeCapacity = 6
    livingSpaceCapacity = 4
    initialNoOfOccupants = 0

    def createRoom(self, name, floor, roomType):

        if roomType == "living space":
            newRoom = LivingSpace(name=name, floor=floor, noOfOccupants=
                self.initialNoOfOccupants, capacity=self.livingSpaceCapacity)
        else:
            newRoom = Office(name=name, floor=floor, noOfOccupants=
                self.initialNoOfOccupants, capacity=self.officeCapacity)
        return newRoom

    def addPerson(self, identifier, firstName, lastName, employeeType):
        if employeeType == "staff":
            newPerson = Staff(identifier=identifier, firstName=firstName, 
                lastName=lastName)
        else:
            newPerson = Fellow(identifier=identifier, firstName=firstName, 
                lastName=lastName)
        return newPerson