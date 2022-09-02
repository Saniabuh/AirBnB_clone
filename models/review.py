#!/usr/bin/python3
"""This module holds the review class"""

from models.base_model import BaseModel
from models.place import Place
from models.user import User


class Review(BaseModel):
    """Implementation of the review class"""

    place_id = ""
    user_id = ""
    text = ""
