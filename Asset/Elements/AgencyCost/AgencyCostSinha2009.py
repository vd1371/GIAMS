from .BaseAgencyCost import BaseAgencyCost
from utils.PredictiveModels.Linear import Linear
from utils.GeneralSettings import *

# All of the formulas are based on imperial system
# The conversions are made to turn them to metric system

def meter_to_feet(val):
	return val * 3.28

class DeckCosts(BaseAgencyCost):

	def __init__(self):
		self.linear_model = Linear(1, 0)
		pass

	def maintenance_costs(self, random):
		cost = 540 + 12.15 * meter_to_feet(self.element.asset.length) * meter_to_feet(self.element.asset.width)
		return cost * self.linear_model.predict_series(random, "deck_maint") / 1000

	def rehabilitation_costs(self, random):

		deck_area = meter_to_feet(self.element.asset.length) * meter_to_feet(self.element.asset.width) / 9
		# Assumption: patchin is more than 15%
		if deck_area < 500:
			unit_cost_1 = 16.09
		elif deck_area >= 500 and deck_area < 2000:
			unit_cost_1 = 10.11
		elif deck_area >= 2000:
			unit_cost_1 = 8.11

		if unit_cost_1 * meter_to_feet(self.element.asset.length) * meter_to_feet(self.element.asset.width) / 1000 < 100:
			unit_cost_2 = 1.2331
		elif unit_cost_1 * meter_to_feet(self.element.asset.length) * meter_to_feet(self.element.asset.width) / 1000 >= 100:
			unit_cost_2 = 0.9311

		return (unit_cost_1 * meter_to_feet(self.element.asset.length) * meter_to_feet(self.element.asset.width) / 1000) * (1 + unit_cost_2 ) * self.linear_model.predict_series(random, "deck_rehab")

	def reconstruction_costs(self, random):
		return meter_to_feet(self.element.asset.length) * meter_to_feet(self.element.asset.width) * 35/1000 * self.linear_model.predict_series(random, "deck_recon")

class SubstructureCosts(BaseAgencyCost):

	def __init__(self):
		self.linear_model = Linear(1, 0)
		pass

	def maintenance_costs(self, random):
		if self.element.asset.road_class == NHS:
			unit_cost = 378
		else:
			unit_cost = 337.7
		return unit_cost * self.linear_model.predict_series(random, "sub_maint") / 1000

	def rehabilitation_costs(self, random):
		return 10 * meter_to_feet(self.element.asset.length) * \
					meter_to_feet(self.element.asset.width) * \
					self.linear_model.predict_series(random, "sub_rehab")

	def reconstruction_costs(self, random):
		# If RC Slab
		if self.element.asset.design == 1 and self.element.asset.material in [5, 6]:
			A, B, C, D = [0.12, 0.727, 0.602, 0.221]
		else:
			A, B, C, D = [0.028, 0.936, 0.983, -0.013]
		return A * meter_to_feet(self.element.asset.length)**B * meter_to_feet(self.element.asset.width) **C *\
					 self.element.asset.vertical_clearance ** D * self.linear_model.predict_series(random, "sub_recon")


class SuperstructureCosts(BaseAgencyCost):

	def __init__(self):
		self.linear_model = Linear(1, 0)
		pass

	def maintenance_costs(self, random):
		if self.element.asset.road_class == NHS:
			unit_cost = 378
		else:
			unit_cost = 337.7
		return unit_cost * self.linear_model.predict_series(random, "super_maint") / 1000

	def rehabilitation_costs(self, random):
		return self.linear_model.predict_series(random, "super_rehab")

	def reconstruction_costs(self, random):
		# If RC Slab
		if self.element.asset.material in [5, 6]:
			A, B, C = [0.04888, 0.899, 1.000]
		elif self.element.asset.material in [1, 2]:
			A, B, C = [0.0513, 0.979, 0.828]
		elif self.element.asset.material in [3]:
			A, B, C = [0.13, 1.00, 0.519]
		elif self.element.asset.material in [4]:
			A, B, C = [0.0885, 0.906, 0.747]

		return A * meter_to_feet(self.element.asset.length)**B * meter_to_feet(self.element.asset.width) **C * self.linear_model.predict_series(random, "super_recon")