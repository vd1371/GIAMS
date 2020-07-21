from utils.GeneralSettings import *

class BaseAgencyCostModel(GenSet):

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

	def predict_series(self, random):
		# This method is called in the simulators
		return {self.MAINT: self.maintenance_costs(random),
				self.REHAB: self.rehabilitation_costs(random),
				self.RECON: self.reconstruction_costs(random)}