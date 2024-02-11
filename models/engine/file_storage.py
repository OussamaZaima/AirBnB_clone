#!/usr/bin/python3
"""A module that defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represents an abstracted storage engine.
    Attributes:
        __file_path (str): the name of the file to save objects to.
        __objects (dict): a dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary representation of __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj_class_name>.id"""
        FileStorage.__objects[f"{type(obj).__name__}.{obj.id}"] = obj

    def save(self):
        """Serializes__objects to the JSON file __file_path."""
        dict_rep = FileStorage.__objects
        obj_dict = {obj: dict_rep[obj].to_dict() for obj in dict_rep.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file __file_path to __objects, if it exist"""
        try:
            with open(FileStorage.__file_path) as f:
                obj_dict = json.load(f)
                for val in obj_dict.values():
                    cls_name = val["__class__"]
                    del val["__class__"]
                    self.new(eval(cls_name)(**val))
        except FileNotFoundError:
            return
