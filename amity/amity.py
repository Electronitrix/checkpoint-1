from __init__ import Room, LivingSpace, Office, Person, Fellow, Staff
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, func
from base import Base

class RoomAllocation(Base):
    """Defines a table that holds mapping of rooms to person"""
    __tablename__ = 'room_allocation'
    id = Column(Integer, primary_key=True)
    roomId = Column(Integer, ForeignKey('room.id'))
    room = relationship(Room)
    personId = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

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

    def checkIfRoomExists(self, name):
        query = session.query(Room).filter_by(name = name).first()
        if query:
            return True
        else:
            return False

    def allocatePersonARoom(self, firstName, lastName, employeeType,
        wantsLivingSpace):
        # can be split into add person
        # add person to office
        # add person to living space
        newPerson = addPerson(firstName, lastName, employeeType)
        successfullyAddedToOffice = addPersonToOffice(newPerson)
        if employeeType == "fellow" and wantsLivingSpace == "Y":
            successfullyAddedToLivingSpace = addPersonToLivingSpace(newPerson)
        message = []
        if not successfullyAddedToOffice and not \
            successfullyAddedToLivingSpace and wantsLivingSpace == "Y":
            return ("There is currently neither an office space or living "
                    "space to allocate to {0} {1}. Please try again later") \
                    .format(firstName, lastName)
        elif not successfullyAddedToOffice:
            message.extend("There is no vacant office space in Amity at the"
                            "moment. Please try again later")
        elif not successfullyAddedToOffice and wantsLivingSpace == "Y":
            message.extend("There is no vacant living space in Amity at the "
                            "moment. Please try again later.")
        elif successfullyAddedToOffice:
            message.extend("{0} {1} was successfully allocated an office " 
                            "space at Amity").format(firstName, lastName)
        elif successfullyAddedToLivingSpace:
            message.extend("{0} {1} was successfully allocated a living "
                            "space at Amity").format(firstName, lastName)
        session.add(newPerson)
        session.commit()
        return " ".join(message)


    def addPerson(self, identifier, firstName, lastName, employeeType):
        if employeeType == "staff":
            newPerson = Staff(identifier=identifier, firstName=firstName, 
                lastName=lastName)
        else:
            newPerson = Fellow(identifier=identifier, firstName=firstName, 
                lastName=lastName)
        return newPerson

    def addPersonToOffice(self, person):
        # attempt to randomly select an office space that is not full
        randomRoom = session.query(Room).filter_by(noOfOccupants < capacity). \
            filter_by(type = "office").order_by(func.rand()).first()
        if not randomRoom:
            return False
        newAllocation = RoomAllocation(room=randomRoom, person=person)
        randomRoom.noOfOccupants += 1
        session.add(newAllocation)
        return True

    def addPersonToLivingSpace(self, person):
        # attempt to randomly select a living space to fellow who indicates interest
        randomRoom = session.query(Room).filter_by(noOfOccupants < capacity). \
            filter_by(type = "living_space").order_by(func.rand()).first()
        if not randomRoom:
            return False
        newAllocation = RoomAllocation(room=randomRoom, person=person)
        randomRoom.noOfOccupants += 1
        session.add(newAllocation)
        return True

    def getPersonIdentifier(self, firstName, lastName):
        """Search database for a person's identifier and return"""
        person = session.query(Person).filter_by(firstName = firstName). \
            filter_by(lastName = lastName).first()
        if not person:
            return "The database does not contain a record for that person."
        else:
            return "Person Identifier: {0}".format(person.id)

    def getPersonRooms(self, personIdentifier):
        """
        Search database for a person's office and living space 
        returns either or both of office name and living space name
        """
        roomAllocations = session.query(RoomAllocation).filter_by(personId = \
            personIdentifier).all()
        if not roomAllocations:
            return "The database does not contain a record for that person."
        output = []
        for counter, room in enumerate(roomAllocations):
            output.extend("Room {0}: {1}\n".format(counter, room))
        return " ".join(output)

    def removePersonFromRoom(self, personIdentifier, roomType):
        """remove person to room allocation from RoomAllocation Table"""
        oldAllocation = session.query(roomAllocations).filter_by(personId =
            personIdentifier).filter_by(type = roomType).first()
        oldRoom = session.query(Room).filter_by(id = oldAllocation.roomId). \
            first()
        oldRoom.noOfOccupants -= 1
        session.delete(oldAllocation)
        return 1
        

    def rellocatePerson(self, personIdentifier, roomName):
        """how can i implement personIdentifier? a combination of first and lastname."""
        """Should it be auto assigned like a primary id?"""
        """how would user find that out?"""
        """User needs to first search for a user."""
        """I need to implement the database of this thing."""
        # that would save my time
        person = session.query(Person).filter_by(id = personIdentifier).first()
        newRoom = session.query(Room).filter_by(name = roomName).first()
        if not newRoom:
            return "Database does not contain the name {0}".format(roomName)
        if newRoom.noOfOccupants >= newRoom.capacity:
            return "{0} is filled up and can not take any more occupants". \
                format(roomName)
        removedSuccessfully = removePersonFromRoom(personIdentifier, \
            newRoom.type)
        if not removedSuccessfully:
            return "Person with that identifier does not exist in database"

        newAllocation = RoomAllocation(room=newRoom, person=person)
        newRoom.noOfOccupants += 1
        session.add(newAllocation)
        session.commit()

    