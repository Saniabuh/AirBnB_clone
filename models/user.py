#!/usr/bin/python3
"""
This module contains a class User
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    Implemenatation of the class User
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
