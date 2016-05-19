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
    identifier = Column(Integer)
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

    def create_person()