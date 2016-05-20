import person

class Fellow(person.Person):
    """Defines the Fellow class"""

    __mapper_args__ = {
        'polymorphic_identity': 'fellow'
    }
