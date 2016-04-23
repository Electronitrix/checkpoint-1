from person import Person

class Fellow(Person):
    """Defines the Fellow class"""

    __mapper_args__ = {
        'polymorphic_identity':'fellow'
    }
    

#Note: both staff and fellows would be assigned office space. but only fellows can  live.
#Once a fellow is added, he should be assigned an office space and living space if he opts for it
#Once a staff is added, he should be assigned an office space