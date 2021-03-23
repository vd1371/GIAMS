#Loading dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .GeneralSettings import *
from .NPV import NPV
from .Container import Container

class AccumulatorThree:
	def __init__(self, **params):
		'''Accumulator object

		This class stores the simulation results,
			draw figures based on them, and possibly store the contents
		Three analysis results are monitores in this accumulator:
			user_costs
			agency_costs
			utilities
		'''
		self.settings = params.pop("settings")
		self.ID = params.pop("ID")
		self.elements = params.pop("elements")
		self.elements_util_weight = params.pop("elements_util_weight")

		self.refresh()
		
	def refresh(self):
		self.meta_data = {}
		self.meta_data['user_costs'] = Container(settings = self.settings)
		self.meta_data['agency_costs'] = Container(settings = self.settings)
		self.meta_data['asset_utils'] = Container(settings = self.settings)

		self.meta_data['elements_costs'] = [Container(settings = self.settings) for _ in range(self.settings.n_elements)]
		self.meta_data['elements_utils'] = [Container(settings = self.settings) for _ in range(self.settings.n_elements)]
		self.meta_data['elements_conds'] = [Container(settings = self.settings) for _ in range(self.settings.n_elements)]

	def update(self, user_costs_stepwise,
					elements_costs_stepwise,
					elements_utils_stepwise,
					elements_conds_stepwise):
	
		# Updating other costs
		self.meta_data['user_costs'].add_to_npv_samples(NPV(user_costs_stepwise,
															self.settings.dt,
															self.settings.discount_rate))
		self.meta_data['user_costs'].update_stepwise(user_costs_stepwise)

		# Updating elements, agency and asset info
		cost_holder, util_holder = 0, 0
		for elem_idx, (costs, utils, conds) in enumerate(zip(elements_costs_stepwise,
															elements_utils_stepwise,
															elements_conds_stepwise)):
			
			npv_cost = NPV(costs, self.settings.dt, self.settings.discount_rate)
			npv_util = NPV(utils, self.settings.dt, self.settings.discount_rate)
			cost_holder += npv_cost
			util_holder += npv_util * self.elements_util_weight[elem_idx]

			self.meta_data['elements_costs'][elem_idx].add_to_npv_samples(npv_cost)
			self.meta_data['elements_utils'][elem_idx].add_to_npv_samples(npv_util)

			self.meta_data['elements_costs'][elem_idx].update_stepwise(costs)
			self.meta_data['elements_utils'][elem_idx].update_stepwise(utils)
			self.meta_data['elements_conds'][elem_idx].update_stepwise(conds)

		self.meta_data['agency_costs'].add_to_npv_samples(cost_holder)
		self.meta_data['asset_utils'].add_to_npv_samples(util_holder)

		self.meta_data['agency_costs'].update_stepwise(np.sum(elements_costs_stepwise, axis = 0))
		self.meta_data['asset_utils'].update_stepwise(np.dot(self.elements_util_weight, elements_utils_stepwise))


	def log_results(self, logger, directory):
		'''Logging the results and saving the figures'''
		for idx in range(self.settings.n_elements):
			logger.info(f"Asset {self.ID} - Element {self.elements[idx].name} "\
							f"costs: Mean, Stdv:{self.elements_costs[idx].expected()}")
			logger.info(f"Asset {self.ID} - Element {self.elements[idx].name} "\
							f"utils: Mean, Stdv:{self.elements_utils[idx].expected()}")

		logger.info(f"Asset {self.ID} - Other costs: Mean, Stdv:{self.meta_data['user_costs'].expected()}")
		logger.info(f"Asset {self.ID} - Agency costs: Mean, Stdv:{self.meta_data['agency_costs'].expected()}")
		logger.info(f"Asset {self.ID} - Total utils Mean, Stdv:{self.meta_data['asset_utils'].expected()}")


		cols = ['User costs', 'Agency costs']
		for idx in range(self.settings.n_elements):
			cols.append(self.elements[idx].name + "Costs")
		for idx in range(self.settings.n_elements):
			cols.append(self.elements[idx].name + "Utils")
		cols += ['Total utils']

		column_values = [self.meta_data['user_costs'].npv_samples, self.meta_data['agency_costs'].npv_samples] + \
						[ls.get_samples() for ls in self.meta_data['elements_costs']] + \
						[ls.get_samples() for ls in self.meta_data['elements_utils']] + \
						[self.meta_data['asset_utils'].get_samples()]


		df = pd.DataFrame(np.transpose(column_values), columns = cols)
		df.to_csv(directory + f"/Bridge{self.ID}-SimulationResults.csv")

		plt.clf()
		df.hist(density = False,  figsize=(20, 10))
		plt.savefig(directory + f"/Bridge{self.ID}-Histogram.png")

	def __repr__(self):
		return "Not yet implemented"
	
	def __str__(self):
		return "Not yet implemented"





