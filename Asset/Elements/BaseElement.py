from utils.GeneralSettings import *

class BaseElement(object):

	def __init__(self, **params):
		super().__init__()
		
		self.name = params.pop('name')
		self.initial_condition = int(params.pop('initial_condition'))
		self.age = params.pop('age')
		self.initial_age = self.age
		self.settings = params.pop('settings')

	def refresh_age(self):
		self.age = self.initial_age

	def set_age(self, new_age):
		self.age = new_age

	def add_age(self, incremenet):
		self.age += incremenet
	
	def __repr__(self):
		return f"{self.name}-CR:{self.initial_condition}-Age:{self.age}"

