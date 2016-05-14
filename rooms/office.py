from room import Room

class Office(Room):
    """Defines attributes and class definition for the Office class"""

    __mapper_args__ = {
        'polymorphic_identity':'office'
    }
