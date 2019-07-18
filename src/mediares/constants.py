"""Global constants."""

import enum


class Gender(enum.Enum):
    """Constants for representing Gender."""

    MALE = enum.auto()
    FEMALE = enum.auto()

    def __repr__(self):
        """Represent the enum member without its value."""
        return f'{self.__class__.__name__}.{self.name}'
