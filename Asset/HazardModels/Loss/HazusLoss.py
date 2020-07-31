import numpy as np
from .BaseHazardLoss import BaseHazardLoss

class HazusLoss(BaseHazardLoss):

	def __init__(self):
		super().__init__()

	def direct_economic_loss(self, ds, replacement_value):
		
		# Based on Hazus
		damage_ratios = {'ds1': 0,
						'ds2': 0.03,
						'ds3': 0.08,
						'ds4': 0.25,
						'ds5': min(2/self.asset.n_spans, 1)}

		return damage_ratios[ds] * replacement_value

	def indirect_costs(self, ds, replacement_value):
		return 0

	def casualties_costs(self, ds, replacement_value):
		# Given the inadequacy of the models provided in the hazus, this section has been left blank
		return 0

	def predict_series(self, ds, random = True):
		
		replacement_value = self.asset.replacement_value.predict_series(random, "total_costs in hazard loss")
		
		direct = self.direct_economic_loss(ds, replacement_value)

		return direct