from room import Room


class LivingSpace(Room):
    """Defines attributes and class definition for the LivingSpace class"""

    __mapper_args__ = {
        'polymorphic_identity': 'living space'
    }
