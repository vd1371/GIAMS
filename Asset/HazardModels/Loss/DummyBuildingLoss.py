#Loading dependencies
import numpy as np
from .BaseHazardLoss import BaseHazardLoss

class DummyLoss(BaseHazardLoss):

	def __init__(self, **params):
		super().__init__(**params)

	def direct_economic_loss(self, ds, replacement_value):
		'''Set the direct economic costs'''
		# Based on Hazus
		damage_ratios = {'ds1': 0,
						'ds2': 0.1,
						'ds3': 0.4,
						'ds4': 0.7,
						'ds5': 1}

		return damage_ratios[ds] * replacement_value

	def indirect_costs(self):
		'''Set the indirect economic costs'''
		return 10

	def casualties_costs(self):
		'''Set the casualties costs'''
		# Given the inadequacy of the models provided in the hazus, this section has been left blank
		return 1000

	def predict_series(self, ds, random = True):
		'''Returning the life replacement costs in a life cycle'''
		replacement_value = self.asset.replacement_value.predict_series(random, "total_costs in hazard loss")
		
		direct = self.direct_economic_loss(ds, replacement_value)

		return direct + self.indirect_costs + self.casualties_costs