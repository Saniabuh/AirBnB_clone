#!/usr/bin/python3
"""This module holds the city class"""

from base_model import BaseModel
from models.state import State


class City(BaseModel):
    """Implementation of the city class"""

    state_id = ""
    name = ""
