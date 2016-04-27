from sqlalchemy import Column, Integer, String, ForeignKey
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from base import Base

class Person(Base):
    """Defines attributes and methods for the Person class"""
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    identifier = Column(Integer)
    firstName = Column(String(20))
    lastName = Column(String(20))
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'person'
    }
