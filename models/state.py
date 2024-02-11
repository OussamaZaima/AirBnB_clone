#!/usr/bin/python3
"""A module that defines the State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents the state class.
    Attributes:
        name (str): name of the state.
    """

    name = ""
