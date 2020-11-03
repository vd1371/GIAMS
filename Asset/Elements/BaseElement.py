from utils.GeneralSettings import *

class BaseElement(object):

	def __init__(self, name = None, initial_condition = None, age = 0):
		super().__init__()
		
		self.name = name
		self.initial_condition = int(initial_condition)
		self.age = age
		self.initial_age = age

	def refresh_age(self):
		self.age = self.initial_age

	def set_age(self, new_age):
		self.age = new_age

	def add_age(self, incremenet):
		self.age += incremenet
	
	def __repr__(self):
		return f"{self.name}-CR:{self.initial_condition}-Age:{self.age}"

