import numpy as np
from utils.GeneralSettings import GenSet

class HazusLossModel(GenSet):

	def __init__(self, n_spans):
		super().__init__()

		self.n_spans = n_spans

	def direct_economic_loss(self, ds, replacement_value):
		
		# Based on Hazus
		damage_ratios = {'ds1': 0,
						'ds2': 0.03,
						'ds3': 0.08,
						'ds4': 0.25,
						'ds5': min(2/self.n_spans, 1)}

		return damage_ratios[ds] * replacement_value

	def indirect_costs(self, ds, replacement_value):
		return 0

	def casualties_costs(self, ds, replacement_value):
		# Given the inadequacy of the models provided in the hazus, this section has been left blank
		return 0

	def total_costs(self, ds, replacement_value):
		direct = self.direct_economic_loss(ds, replacement_value)
		indirect = self.indirect_costs(ds, replacement_value)
		casualties = self.casualties_costs(ds, replacement_value)

		return direct + indirect + casualties