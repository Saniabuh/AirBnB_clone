#!/usr/bin/python3
"""
This module containsa class FileStorage
"""

import json
from models.base_model import BaseModel
from models.user import User

classes = {"BaseModel": BaseModel, "User": User}


class FileStorage:
    """
    Implementation of the class
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        """
        if obj:
            key = obj.__class__.__name__ + "." + obj.id
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        json_obj = {}
        for key in self.__objects:
            json_obj[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_obj, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON
        file (__file_path) exists
        """
        try:
            with open(self.__file_path, 'r') as f:
                j_obj = json.load(f)
            for k in j_obj:
                self.__objects[k] = classes[j_obj[k]["__class__"]](**j_obj[k])
        except Exception:
            pass
