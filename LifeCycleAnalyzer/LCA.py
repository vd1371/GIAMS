# Loading dependencies
import os
import numpy as np
import matplotlib.pyplot as plt
from .BaseLCA import BaseLCA

class LCA(BaseLCA):

	def __init__(self, **params):
		super().__init__(**params)
		'''The first monte carlo analyzer in GIAMS

		This module conducts life cycle analysis with the
			help of a simulator
		
		::params::
		random: whether the analysis should be done stochastically
		is_hazard: whether the hazard should be considered or not
		n_simulations: number of simulation rounds for monte carlo
		'''

		self.random = params.pop("random", True)
		self.is_hazard = params.pop('is_hazard', True)
		self.n_simulations = params.pop('n_simulations')

	def run(self, n_simulations = None, random = False, verbose = False):

		N = self.n_simulations if n_simulations is None else n_simulations

		for asset in self.network.assets:
			
			for i in range(N):

				if verbose and i % 1000 == 0:
					print (f"Simulation {i} is done")

				user_costs_stepwise, elements_costs_stepwise, \
					elements_utils_stepwise, elements_conds_stepwise = \
						self.simulator.get_one_instance(asset, self.is_hazard, random = self.random)
				
				asset.accumulator.update(user_costs_stepwise, elements_costs_stepwise,
										elements_utils_stepwise, elements_conds_stepwise)

	def run_for_one_asset(self, asset, n_simulations = None):
		N = self.n_simulations if n_simulations is None else n_simulations

		asset.accumulator.refresh()
		for i in range(N):
			user_costs_stepwise, elements_costs_stepwise, \
				elements_utils_stepwise, elements_conds_stepwise = \
					self.simulator.get_one_instance(asset, is_hazard= False, random = self.random)
			asset.accumulator.update(user_costs_stepwise, elements_costs_stepwise,
										elements_utils_stepwise, elements_conds_stepwise)

	def get_network_npv(self):
		
		network_user_costs = 0
		network_agency_costs = 0
		network_util = 0

		for asset in self.network.assets:

			network_user_costs += asset.accumulator.meta_data['user_costs'].expected()[0]
			network_agency_costs += asset.accumulator.meta_data['agency_costs'].expected()[0]
			network_util += asset.accumulator.meta_data['asset_utils'].expected()[0]

		return network_user_costs, network_agency_costs, network_util

	def get_network_util_holism(self):

		network_cond_after = np.zeros((self.settings.n_elements, self.settings.n_steps))
		network_cond_before = np.zeros(self.settings.n_elements).reshape(-1, 1)

		# Summation of the conditions of the condition ratings
		# TODO: Consider not assessing the effect of recovery
		for asset in self.network.assets:
			for element_idx, element_conds in enumerate (asset.accumulator.elements_conds):
				network_cond_after[element_idx] += element_conds.get_stepwise()

			for element_idx, element in enumerate (asset.elements):
				network_cond_before[element_idx][0] += element.initial_condition

		# Getting the average by dividing by the number of assets
		network_cond_after = network_cond_after / self.network.n_assets
		network_cond_before = network_cond_before / self.network.n_assets
		network_cond_before = np.concatenate((network_cond_before, network_cond_after), axis = 1)
		network_cond_before = network_cond_before[:, :-1]

		network_util_stepwise = np.zeros((self.settings.n_elements, self.settings.n_steps))
		# Converting the conditions to utility
		for element_idx, element in enumerate(self.network.assets[0].elements):
			network_util_stepwise[element_idx] = \
				element.utility_model.get(network_cond_before[element_idx], network_cond_after[element_idx])

		network_util_holism = np.sum(network_util_stepwise, axis = 1)
		network_util_holism = np.dot(self.network.assets[0].elements_util_weight, network_util_holism) * \
									self.network.n_assets
		return network_util_holism

	def get_network_stepwise(self):

		network_user_costs = np.zeros(self.settings.n_steps)
		network_agency_costs = np.zeros(self.settings.n_steps)
		network_util = np.zeros(self.settings.n_steps)

		for asset in self.network.assets:
			
			network_user_costs += asset.accumulator.meta_data['user_costs'].get_stepwise()
			network_agency_costs += asset.accumulator.meta_data['agency_costs'].get_stepwise()
			network_util += asset.accumulator.meta_data['asset_utils'].get_stepwise()

		return network_user_costs, network_agency_costs, network_util

	def get_year_0(self):

		year0_user_costs, year0_agency_costs, year0_utils = 0, 0, 0

		for asset in self.network.assets:

			year0_user_costs += asset.accumulator.meta_data['user_costs'].at_year(0)
			year0_agency_costs += asset.accumulator.meta_data['agency_costs'].at_year(0)
			year0_utils = asset.accumulator.meta_data['asset_utils'].at_year(0)

		return year0_user_costs, year0_agency_costs, year0_utils

	def check_budget(self):

		# TO check if the MRR action is in the budget of the network
		def exceed_yearly_budget_against_costs(budgets, costs):

			for budget, cost in zip(budgets, costs):
				if cost > budget:
					return True
			return False

		_, npv_agency_costs, _ = self.get_network_npv() 
		_, agency_costs, _ = self.get_year_0()

		if agency_costs > self.network.current_budget_limit:
			# To check whether the plan meets the current budget
			return False

		elif npv_agency_costs > self.network.npv_budget_limit:
			# To put a cap on the npv of the MRR plan
			return False

		elif exceed_yearly_budget_against_costs(self.network.budget_model.predict_series(random = False), 
												self.get_network_stepwise()[1]):
			# To check whether the predicted costs and budget suits each other
			return False

		elif npv_agency_costs == 0:
			# Check if at least one action is chosed
			return False
		return True

	def log_results(self):

		# Logging each asset independently
		print ("Logging the results")
		self.log.info(f"The results of the life cycle analysis: {self.lca_name}")

		for asset in self.network.assets:
			asset.accumulator.log_results(self.log, self.directory)
			self.log.info(f"MRR: {asset.mrr_model.mrr_to_decimal()}")

		# Logginf the network
		N = self.network.assets[0].accumulator.meta_data['user_costs'].simulator_counter

		user_costs = np.zeros(N)
		agency_costs = np.zeros(N)
		network_utils = np.zeros(N)

		for asset in self.network.assets:
			user_costs += asset.accumulator.meta_data['user_costs'].get_samples()
			agency_costs += asset.accumulator.meta_data['agency_costs'].get_samples()
			network_utils += asset.accumulator.meta_data['asset_utils'].get_samples()

		self.log.info(f"The network user costs Mean: {round(np.mean(user_costs),2)} , Stdv:{round(np.std(user_costs),2)}")
		self.log.info(f"The network agency costs Mean: {round(np.mean(agency_costs),2)} , Stdv:{round(np.std(agency_costs),2)}")
		self.log.info(f"The network utils Mean: {round(np.mean(network_utils),2)} , Stdv:{round(np.std(network_utils),2)}")

		year0_user_costs, year0_agency_costs, year0_utils  =self.get_year_0()

		self.log.info(f"At year 0 - user costs: {year0_user_costs:.2f}, agency costs : {year0_agency_costs}, util: {year0_utils:.2f}")

		plt.clf()
		plt.hist(user_costs)
		plt.savefig(self.directory + f"/NetworkUserCostHistogram.png")

		plt.clf()
		plt.hist(agency_costs)
		plt.savefig(self.directory + f"/NetworkAgencyCostHistogram.png")

		plt.clf()
		plt.hist(network_utils)
		plt.savefig(self.directory + f"/NetworkUtilsHistogram.png")

	

	def get_objective1(self):
		return self.network.objective1()

	def get_objective2(self):
		return self.network.objective2()




	