#!/usr/bin/python3
"""A module that defines the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents the User class.
    Attributes:
        email (str): email of the user.
        password (str): password of the user.
        first_name (str): first name of the user.
        last_name (str): last name of the user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
