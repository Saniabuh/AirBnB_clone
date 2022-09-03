#!/usr/bin/python3

"""
__init__ for model package
"""

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
