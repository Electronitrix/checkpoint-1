from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
frin sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Person(Base):
    """Defines attributes and methods for the Person class"""
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    firstName = Column(String(20))
    lastName = Column(String(20))
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_on':type,
        'polymorphic_identity':'person'
    }

engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)