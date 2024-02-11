#!/usr/bin/python3
"""A module that defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represents a city class.
    Attributes:
        state_id (str): the state id.
        name (str): name of the city.
    """

    state_id = ""
    name = ""
