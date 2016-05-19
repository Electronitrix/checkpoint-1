from person import Person


class Fellow(Person):
    """Defines the Fellow class"""

    __mapper_args__ = {
        'polymorphic_identity': 'fellow'
    }
