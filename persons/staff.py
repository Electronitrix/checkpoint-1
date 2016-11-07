import person


class Staff(person.Person):
    """Defines the Staff class"""
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }
