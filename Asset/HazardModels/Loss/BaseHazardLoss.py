#Loading dependencies
import numpy as np

class BaseHazardLoss:
	def __init__(self, **params):
		'''Parent object for all future hazard loss models
		
		::params::
		settings
		'''
		self.settings = params.pop('settings')

	def set_asset(self, asset):
		self.asset = asset

	def direct_costs(self):
		raise NotImplementedError ("direct_costs is not implemented yet")

	def indirect_costs(self):
		raise NotImplementedError ("indirect_costs is not implemented yet")

	def casualties_costs(self):
		raise NotImplementedError ("casaulties_costs is not implemented yet")

	def predict_series(self):
		raise NotImplementedError ("rpedict_series is not implemented yet")