import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .GeneralSettings import GenSet, NPV

class Container(GenSet):
	
	def __init__(self):
		self.npv_samples = []
		self.stepwise = np.zeros(self.n_steps)
		self.simulator_counter = 0

	def add_to_stepwise(self, stepwise_vals):
		for idx in range(self.n_steps):
			self.stepwise[idx] = (self.stepwise[idx] * self.simulator_counter + stepwise_vals[idx]) / (self.simulator_counter + 1)
		self.simulator_counter += 1

	def add_to_npv_samples(self, val):
		self.npv_samples.append(val)

	def at_year(self, year = 0):
		idx = int(year/self.dt)
		return self.stepwise[idx]

	def expected(self):
		return round(np.average(np.array(self.npv_samples)),2), round(np.std(np.array(self.npv_samples)),2)

	def get_samples(self):
		return self.npv_samples

	def get_stepwise(self):
		return self.stepwise

class Accum(GenSet):
	'''
	This class stores the simulation results, draw figures based on them, and possibly store the contents
	'''
	
	def __init__(self, ID, elements, elements_util_weight):
		self.ID = ID
		self.elements = elements
		self.elements_util_weight = elements_util_weight

		self.refresh()
		
	def refresh(self):
		self.user_costs = Container()
		self.agency_costs = Container()
		self.asset_utils = Container()

		self.elements_costs = [Container() for _ in range(self.n_elements)]
		self.elements_utils = [Container() for _ in range(self.n_elements)]


	def update(self, user_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise):

		# Updating other costs
		self.user_costs.add_to_npv_samples(NPV(user_costs_stepwise, self.dt, self.discount_rate))
		self.user_costs.add_to_stepwise(user_costs_stepwise)

		# Updating elements, agency and asset info
		cost_holder, util_holder = 0, 0
		for idx, (costs, utils) in enumerate(zip(elements_costs_stepwise, elements_utils_stepwise)):
			
			npv_cost = NPV(costs, self.dt, self.discount_rate)
			npv_util = NPV(utils, self.dt, self.discount_rate)
			cost_holder += npv_cost
			util_holder += npv_util * self.elements_util_weight[idx]

			self.elements_costs[idx].add_to_npv_samples(npv_cost)
			self.elements_utils[idx].add_to_npv_samples(npv_util)

			self.elements_costs[idx].add_to_stepwise(costs)
			self.elements_utils[idx].add_to_stepwise(utils)

		self.agency_costs.add_to_npv_samples(cost_holder)
		self.asset_utils.add_to_npv_samples(util_holder)

		self.agency_costs.add_to_stepwise(np.sum(elements_costs_stepwise, axis = 0))
		self.asset_utils.add_to_stepwise(np.dot(self.elements_util_weight, elements_utils_stepwise))


	def log_results(self, logger, directory):
		for idx in range(self.n_elements):
			logger.info(f"Asset {self.ID} - Element {self.elements[idx].name} costs: Mean, Stdv:{self.elements_costs[idx].expected()}")
			logger.info(f"Asset {self.ID} - Element {self.elements[idx].name} utils: Mean, Stdv:{self.elements_utils[idx].expected()}")
		
		logger.info(f"Asset {self.ID} - Other costs: Mean, Stdv:{self.user_costs.expected()}")
		logger.info(f"Asset {self.ID} - Agency costs: Mean, Stdv:{self.agency_costs.expected()}")
		logger.info(f"Asset {self.ID} - Total utils Mean, Stdv:{self.asset_utils.expected()}")


		cols = ['Other costs', 'Agency costs']
		for idx in range(self.n_elements):
			cols.append(self.elements[idx].name + "Costs")
		for idx in range(self.n_elements):
			cols.append(self.elements[idx].name + "Utils")
		cols += ['Total utils']

		column_values = [self.user_costs.npv_samples, self.agency_costs.npv_samples] + \
						[ls.get_samples() for ls in self.elements_costs] + \
						[ls.get_samples() for ls in self.elements_utils] + \
						[self.asset_utils.get_samples()]


		df = pd.DataFrame(np.transpose(column_values), columns = cols)
		df.to_csv(directory + f"/Bridge{self.ID}-SimulationResults.csv")

		plt.clf()
		df.hist(density = False,  figsize=(20, 10))
		plt.savefig(directory + f"/Bridge{self.ID}-Histogram.png")

	def __repr__(self):
		return "Not yet implemented"
	
	def __str__(self):
		return "Not yet implemented"





