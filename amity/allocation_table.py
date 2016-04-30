from sqlalchemy import Table, Column, Integer, ForeignKey
from base import Base

allocation_table = Table('allocation_table',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('roomId', Integer, ForeignKey('room.id')),
    Column('personId', Integer, ForeignKey('person.id'))
)
