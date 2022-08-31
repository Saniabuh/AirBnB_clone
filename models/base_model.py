#!/usr/bin/python3

from uuid import uuid4 as uid
from datetime import datetime

class BaseModel:
	def __init__(self):
	     self.id = uid()
	     self.created_at = datetime()
	     self.updated_at =
