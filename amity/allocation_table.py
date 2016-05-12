from sqlalchemy import Table, Column, Integer, ForeignKey
from base import Base

allocation_table = Table('allocation_table',
    Base.metadata,
    Column('roomId', Integer, ForeignKey('room.id'), primary_key=True),
    Column('personId', Integer, ForeignKey('person.id'), primary_key=True)
)