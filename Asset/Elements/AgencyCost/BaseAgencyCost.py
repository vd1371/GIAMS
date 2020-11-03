from utils.GeneralSettings import *

class BaseAgencyCost(GenSet):

	def __init__(self):
		pass

	def set_element(self, element):
		self.element = element

	def maintenance_costs(self):
		raise NotImplementedError ("maintenance_costs model is not implemented yet")

	def rehabilitation_costs(self):
		raise NotImplementedError ("rehabilitation_costs model is not implemented yet")

	def reconstruction_costs(self):
		raise NotImplementedError ("reconstruction_costs model is not implemented yet")

	def predict_series(self):
		raise NotImplementedError ("predict_series model is not implemented yet")