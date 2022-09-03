#!/usr/bin/python3
from datetime import datetime
import models
import uuid
"""
A module that defines a base class
with all common attributes/method for other classes
"""


class BaseModel():
    """
    A base class for other classes
    defines all attributes/method
    all subclasses could inherit from
    """
    def __init__(self, *args, **kwargs):
        """
        A class constructor
        initializes the private instance variables
        assigns new values to the variables
        if no kwargs was passed
        sets the **kwargs if it exists
        using iteration
        self.kwargs[key] = value
        """
        self.number = 0
        self.name = type(self).__name__
        self.updated_at = datetime.now()
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()

        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, key, value)

        else:
            models.storage.new(self)

    def save(self):
        """A base class that updates the \"self.updated_at\"
        to the current time when the object was saved
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        A method that returns a dictionary
        containing all keys/values of __dict__ instance
        with some added parameters
        A key __class__ added
        Created_at and Updated_at:
            converted to string object in ISO format using .isoformat()
        """
        new_dict = self.__dict__.copy()
        new_dict['name'] = self.name
        new_dict['__class__'] = self.name
        new_dict['updated_at'] = self.updated_at.isoformat()
        new_dict['created_at'] = self.created_at.isoformat()
        return new_dict

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
