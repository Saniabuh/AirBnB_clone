#!/usr/bin/python3
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage():
    """
    deserializes instance of a JSON FILE
    serializes instance to a JSON FILE
    """

    __objects = {}
    __file_path = 'file.json'
    __file_path2 = 'storage.json'

    def all(self):
        """Returns the __objects dict"""
        return type(self).__objects

    def new(self, obj):
        """Adds obj in the __objects dict"""
        key = obj.__class__.__name__ + "." + obj.id
        type(self).__objects[key] = obj

    def destroy(self, arg="None"):
        """deletes the storage"""
        if arg == "None":
            type(self).__objects.clear()
        else:
            type(self).__objects.pop(arg)

    def save(self):
        """serializes __objects to __file_path"""
        with open(type(self).__file_path, "w", encoding='utf-8') as file:
            dictionary = {}
            for key, value in type(self).__objects.items():
                dictionary[key] = value.to_dict()
            # type(self).__objects.clear()
            json.dump(dictionary, file, indent=2)
        with open(type(self).__file_path2, "w") as file1:
            dictionary1 = {}
            for key, value in type(self).__objects.items():
                dictionary1[key] = value
            json.dump(dictionary1, file1, indent=2, default=str)

    def reload(self):
        """
        deserializes the json file to __objects
        only if the json file exists
        otherwise do nothing if the file doesn't exists
        no exception is raised
        """
        try:
            with open(self.__file_path, 'r') as file:
                value = json.load(file)
                # self.__objects.update(value)
                # file.close()
                for object in value.values():
                    class_name = object['__class__']
                    del object['__class__']
                    self.new(eval(class_name)(**object))
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return
