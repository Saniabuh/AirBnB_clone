#!/usr/bin/python3

from datetime import datetime
from uuid import uuid4

class BaseModel():
	def __init__(self):
	     self.id = str(uuid4())
	     self.created_at = datetime.now()
	     self.updated_at = datetime.now()
	     self.name = __class__.__name__
	     self.my_number = my_number
	def __str__(self):
		return "[{}] ({}) {}" .format(
					     BaseModel.__name__,
					     self.id,
					     self.__dict__)
	def save(self):
	    self.updated_at = datetime.now()

	def to_dict(self):
		
	new_dict = self.__dict__
        new_dict['__class__'] = BaseModel.__name__
	new_dict['created_at'] = new_dict['created_at'].isoformat()
	new_dict['updated_at'] = new_dict['updated_at'].isoformat()
	if my_number in new_dict.keys():
	 new_dict['my_number'] = int(new_dict['my_number'])
	return new_dict

my_model = BaseModel()
my_model.name = "My First Model"
my_model.my_number = 89
print(my_model)
my_model.save()
print(my_model)
my_model_json = my_model.to_dict()
