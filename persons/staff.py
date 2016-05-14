from person import Person

class Staff(Person):
    """Defines the Staff class"""
    __mapper_args__ = {
        'polymorphic_identity':'staff'
    }