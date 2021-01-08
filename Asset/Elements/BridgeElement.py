import numpy as np
from .BaseElement import *

class BridgeElement(BaseElement):

	def __init__(self, **params):
		super().__init__(**params)

		for key, value in params.items():
			setattr(self, key, value)

	def set_asset(self, asset):
		self.asset = asset

	def set_condition_rating_model(self, model):
		self.conditon_rating_model = model

	def set_deterioration_model(self, model):
		# To set the asset to the deterioration model
		model.set_asset(self.asset)

		# To set the element to the deterioration model
		model.set_element(self)
		self.deterioration_model = model

	def set_utility_model(self, model):
		self.utility_model = model

	def set_agency_costs_model(self, model):
		# To set the element to the agency costs model
		model.set_element(self)
		self.agency_cost_model = model
	