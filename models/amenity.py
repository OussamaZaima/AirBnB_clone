#!/usr/bin/python3
"""A module that defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent the amenity class.
    Attributes:
        name (str): name of amenity.
    """

    name = ""
