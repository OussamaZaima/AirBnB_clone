#!/usr/bin/python3
"""A module that defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents the review class.
    Attributes:
        place_id (str): place id.
        user_id (str): user id.
        text (str): text of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
