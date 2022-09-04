#!/usr/bin/python3

"""
A module that defines a class FileStorage for database engine
"""

import json
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to instances
    Attr:
        __file_path (str): path to the JSON file
        __objects (dictionary): empty dictionary,
        stores object with key as '<class name>.id
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Return:
            dictionary (dict): __objects attribute
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        Attr:
            obj (BaseModel): instance obj
        """
        key = "{:s}.{:s}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def clean(self):
        """Resets the private __object to an empty dictionary"""
        self.__objects = {}

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        objs = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, mode='w', encoding='utf-8') as j_file:
            j_file.write(json.dumps(objs))

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file exits)
        """
        try:
            with open(self.__file_path, mode='r', encoding='utf-8') as j_file:
                data = j_file.read()
            if data != "" and data is not None:
                data = json.loads(data)
                for value in data.values():
                    Clazz = eval(value['__class__'])
                    self.new(Clazz(**value))
        except FileNotFoundError:
            pass
