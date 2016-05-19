from os import sys, path

from sqlalchemy import Column, Integer, String

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from base import Base


class Room(Base):
    """Defines attributes and methods for the Room class"""
    __tablename__ = 'room'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    identifier = Column(Integer)
    name = Column(String(50))
    floor = Column(Integer)
    no_of_occupants = Column(Integer, default=0)
    capacity = Column(Integer)
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'room'
    }
