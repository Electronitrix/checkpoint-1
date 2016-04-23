from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Room(Base):
    """Defines attributes and methods for the Room class"""
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    floor = Column(Integer)
    noOfOccupants = Column(Integer)
    capacity = Column(Integer)
    type = Column(String(20))
        
    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'room'
    }

class RoomAllocaction(Base):
    """Defines a table that holds mapping of rooms to person"""
    __tablename__ = 'room_allocation'
    id = Column(Integer, primary_key=True)
    roomId = Column(Integer, ForeignKey('room.id'))
    room = relationship(Room)
    personId = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)


engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)