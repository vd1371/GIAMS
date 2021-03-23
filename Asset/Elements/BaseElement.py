'''The parent class of all future written elemtns'''
from utils.GeneralSettings import *

class BaseElement(object):

	def __init__(self, **params):
		super().__init__()

		for key, value in params.items():
			setattr(self, key, value)

		if hasattr(self, 'age'):
			self.initial_age = self.age
		else:
			raise ValueError ("Elements must have age. Consider passing"
								" age when instantiating elements")

	def refresh_age(self):
		'''To reset the age of the element after replacement'''
		self.age = self.initial_age

	def set_age(self, new_age):
		'''To set the age of elements'''
		self.age = new_age

	def add_age(self, incremenet):
		'''To incerementally increase the age'''
		assert isinstance(incremenet, int), 'incremenet must be integer'
		self.age += incremenet

	def set_asset(self, asset):
		'''To introdcue the asset to the elements'''
		if not 'AssetTypes' in str(type(asset)):
			raise ValueError("You must pass an asset type like bridge here")
		self.asset = asset

	def set_condition_rating_model(self, model):
		'''To set the condition rating to the model'''
		if not 'ConditionRating' in str(type(model)):
			raise ValueError("You must pass a condition rating type here")
		self.conditon_rating_model = model

	def set_deterioration_model(self, model):
		'''set the deterioration model'''
		if not 'Deterioration' in str(type(model)):
			raise ValueError("You must pass a deterioration type here")
		model.set_asset(self.asset)

		# To set the element to the deterioration model
		model.set_element(self)
		self.deterioration_model = model

	def set_utility_model(self, model):
		'''To set the utility model'''
		if not 'Utility' in str(type(model)):
			raise ValueError("You must pass a utility type here")
		self.utility_model = model

	def set_agency_costs_model(self, model):
		'''To set the element to the agency costs model'''
		if not 'AgencyCost' in str(type(model)):
			raise ValueError("You must pass a agency cost type here")
		model.set_element(self)
		self.agency_cost_model = model
	
	def __repr__(self):
		'''String representation of the element object'''
		return f"{self.name}-CR:{self.initial_condition}-Age:{self.age}"

