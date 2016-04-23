from __init__ import Room, LivingSpace, Office
# from sqlalchemy import create_engine

# engine = create_engine('sqlite:///:memory:', echo=True)

class Amity(object):
    """Defines the Amity class"""
    def __init__(self):
        self.officeSpaces = []
        self.livingSpaces = []
        self.staff = []
        self.fellows = []

    def createRoom(self, name, floor, roomType):
        officeCapacity = 6
        livingSpaceCapacity = 4

        if roomType == "living space":
            self.livingSpaces.append(LivingSpace(name, floor, roomNo, livingSpaceCapacity))
        else:
            self.officeSpaces.append(Office(name, floor, roomNo, officeCapacity))

    def addPersonToRoom(self, firstName, lastName, employeeType, wantsLivingSpace):
        if employeeType == "staff":
            newPerson = self.staff.append(firstName, lastName)
        else:
            newPerson = self.staff.append(firstName, lastName)

        # attempt to randomly select an office space that is not full
        successfulInGivingPersonOfficeSpace = False

        while not successfulInGivingPersonOfficeSpace:
            indexToAssignedOfficeSpace = random.randint(0, len(self.officeSpaces))
            if self.officeSpaces[indexToAssignedOfficeSpace].noOfOccupants < \
                self.officeSpaces.capacity:
                self.officeSpaces[indexToAssignedOfficeSpace].occupants.append(
                    newPerson)
                self.officeSpaces[indexToAssignedOfficeSpace].noOfOccupants +=\
                    1
                successfulInGivingPersonSpace = True

        # attempt to randomly select a living space to fellow who indicates interest
        if employeeType == "fellow" and wantsLivingSpace:
            successfulInGivingPersonLivingSpace = False

            while not successfulInGivingPersonLivingSpace:
                indexToAssignedLivingSpace = random.randint(0, len(self.livingSpaces))
                if self.livingSpaces[indexToAssignedLivingSpace].noOfOccupants\
                    < self.officeSpaces.capacity:
                    self.livingSpaces[indexToAssignedLivingSpace].occupants. \
                        append(newPerson)
                    self.livingSpaces[indexToAssignedLivingSpace]. \
                        noOfOccupants += 1
                    successfulInGivingPersonLivingSpace = True

    def removePersonFromRoom(self, personIdentifier, roomName):
        pass

    def rellocatePerson(self, personIdentifier, roomName):
        """how can i implement personIdentifier? a combination of first and lastname."""
        """Should it be auto assigned like a primary id?"""
        """how would user find that out?"""
        """User needs to first search for a user."""
        """I need to implement the database of this thing."""
        # that would save my time
        