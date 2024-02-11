#!/usr/bin/python3
"""A module that defines the HBnB console class."""

import re
import cmd
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def HBnB_parse(arg):
    braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            h_lexer = split(arg[:brackets.span()[0]])
            ret = [i.strip(",") for i in h_lexer]
            ret.append(brackets.group())
            return ret
    else:
        h_lexer = split(arg[:braces.span()[0]])
        ret = [i.strip(",") for i in h_lexer]
        ret.append(braces.group())
        return ret


class HBNBCommand(cmd.Cmd):
    """Defines the HBnB command interpreter.
    Attributes:
        prompt (str): custom command prompt.
    """

    prompt = "(hbnb) "
    __class_set = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do not execute anything upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior of module for all valid inputs"""
        arg_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_list = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_list[1])
            if match is not None:
                vcmd = [arg_list[1][:match.span()[0]], match.group()[1:-1]]
                if vcmd[0] in arg_dict.keys():
                    invoke = f"{arg_list[0]} {vcmd[1]}"
                    return arg_dict[vcmd[0]](invoke)
        print(f"*** Unknown syntax: {arg}")
        return False

    def do_quit(self, arg):
        """Quit command for exiting the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal for exiting the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new instance of a class and print its id.
        """
        arg_list = HBnB_parse(arg)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__class_set:
            print("** class doesn't exist **")
        else:
            print(eval(arg_list[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Displays string representation of an instance with a given id.
        """
        arg_list = HBnB_parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__class_set:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif f"{arg_list[0]}.{arg_list[1]}" not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict[f"{arg_list[0]}.{arg_list[1]}"])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Deletes a class instance with a given id."""
        arg_list = HBnB_parse(arg)
        obj_dict = storage.all()
        if len(arg_list) == 0:
            print("** class name missing **")
        elif arg_list[0] not in HBNBCommand.__class_set:
            print("** class doesn't exist **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif f"{arg_list[0]}.{arg_list[1]}" not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict[f"{arg_list[0]}.{arg_list[1]}"]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Displays string representations of all instances of given class.
        If no class is specified, displays all instantiated objects."""
        arg_list = HBnB_parse(arg)
        if len(arg_list) > 0 and arg_list[0] not in HBNBCommand.__class_set:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_list) > 0 and arg_list[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_list) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieves the number of instances of a given class."""
        arg_list = HBnB_parse(arg)
        count = 0
        for obj in storage.all().values():
            if arg_list[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Updates class instance with given id by adding or updating
        a given attribute key/value pair or dictionary."""
        arg_list = HBnB_parse(arg)
        obj_dict = storage.all()

        if len(arg_list) == 0:
            print("** class name missing **")
            return False
        if arg_list[0] not in HBNBCommand.__class_set:
            print("** class doesn't exist **")
            return False
        if len(arg_list) == 1:
            print("** instance id missing **")
            return False
        if f"{arg_list[0]}.{arg_list[1]}" not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_list) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_list) == 3:
            try:
                type(eval(arg_list[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_list) == 4:
            obj = obj_dict[f"{arg_list[0]}.{arg_list[1]}"]
            if arg_list[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_list[2]])
                obj.__dict__[arg_list[2]] = valtype(arg_list[3])
            else:
                obj.__dict__[arg_list[2]] = arg_list[3]
        elif type(eval(arg_list[2])) == dict:
            obj = obj_dict[f"{arg_list[0]}.{arg_list[1]}"]
            for k, v in eval(arg_list[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
