import numpy as np
from utils.GeneralSettings import GenSet

class BaseHazardLossModel(GenSet):

	def __init__(self):
		super().__init__()

	def set_asset(self, asset):
		self.asset = asset

	def direct_costs(self):
		raise NotImplementedError ("direct_costs is not implemented yet")

	def indirect_costs(self):
		raise NotImplementedError ("indirect_costs is not implemented yet")

	def casualties_costs(self):
		raise NotImplementedError ("casaulties_costs is not implemented yet")

	def total_costs(self):
		return np.random.randn(int(self.horizon/self.dt))