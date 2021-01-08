#Loading dependencies
import numpy as np

class BaseAsset:
	def __init__(self, ID = 11111, **kwargs):
		'''Parent object for all future assets

		::params::
		ID: the id of each asset
		settings: the general setting of the analysis
		'''
		self.ID = ID
		for key, value in kwargs.items():
			setattr(self, key, value)

		self.elements = []
		self.set_elements_util_weight()

	def set_elements_util_weight(self, weights = None):
		if weights is None:
			self.elements_util_weight = np.array([1/self.settings.n_elements for _ in range(self.settings.n_elements)])
		else: 
			self.elements_util_weight = weights

	def set_accumulator(self, accumulator):
		self.accumulator = accumulator(ID = self.ID,
										elements = self.elements,
										elements_util_weight = self.elements_util_weight,
										settings = self.settings)

	def refresh_age(self):
		for element in self.elements:
			element.refresh_age()

	def set_mrr_model(self, mrr):
		self.mrr_model = mrr

	def set_user_cost_model(self, model):
		model.set_asset(self)
		self.user_cost_model = model

	def set_hazard_model(self, model):
		self.hazard_model = model

	def add_element(self, element):
		self.elements.append(element)

	def set_replacement_value_model(self):
		raise ValueError ("Replacement value model is not defined yet")
		
	def __repr__(self):
		return f"Asset-{self.ID}"

	