from sqlalchemy import Column, Integer, String, ForeignKey
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from base import Base

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
