#!/usr/bin/python3
"""A module that defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the base model of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initializes an instance of the class.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        time_form = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, time_form)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """Updates the updated_at with attr the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns a dict repre of the BaseModel instance.
        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        ret_dict = self.__dict__.copy()
        ret_dict["created_at"] = self.created_at.isoformat()
        ret_dict["updated_at"] = self.updated_at.isoformat()
        ret_dict["__class__"] = self.__class__.__name__
        return ret_dict

    def __str__(self):
        """Returns the str repre of the BaseModel instance."""
        clname = self.__class__.__name__
        return f"[{clname}] ({self.id}) {self.__dict__}"
