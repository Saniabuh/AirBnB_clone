#!/usr/bin/python3

"""
A subclass module of Basemodel
located in the base_model.py
"""
"""from models.base_model import BaseModel"""
from base_model import models


class City(BaseModel):
    """
    A subclass module of BaseModel
    with some added attributes
    """
    state_id = ""
    name = ""
