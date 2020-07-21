from utils.GeneralSettings import *

class BaseElement(object):

	def __init__(self, name = None, initial_condition = None, age = 0):
		super().__init__()
		
		self.name = name
		self.initial_condition = initial_condition
		self.age = age
		self.conditions_in_horizon = []

	def refresh(self):
		self.conditions_in_horizon = []

	def set_age(self, new_age):
		self.age = new_age

	def add_age(self, incremenet):
		self.age += incremenet

	def append_next_condition(self, con):
		self.conditions_in_horizon.append(con)
	
	def __repr__(self):
		return f"{self.name}-CR:{self.initial_condition}-Age:{self.age}"

