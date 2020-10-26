import os, sys
import logging
import time
import numpy as np
import matplotlib.pyplot as plt

from .BaseLCA import BaseLCA

class LCA(BaseLCA):

	def __init__(self, network = None,
						lca_name = 'Unknown',
						simulator = None,
						log_level = logging.DEBUG,
						random = True,
						is_hazard = True,
						n_simulations = 100,
						should_report = True):
		super().__init__(network, lca_name, simulator, log_level, should_report)

		self.random = random
		self.is_hazard = is_hazard
		self.n_simulations = n_simulations

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
			user_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise = \
				self.simulator.get_one_instance(asset, is_hazard= False, random = self.random)
			asset.accumulator.update(user_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise)

	def get_network_npv(self):
		
		network_user_costs = 0
		network_agency_costs = 0
		network_util = 0

		for asset in self.network.assets:

			network_user_costs += asset.accumulator.user_costs.expected()[0]
			network_agency_costs += asset.accumulator.agency_costs.expected()[0]
			network_util += asset.accumulator.asset_utils.expected()[0]

		return network_user_costs, network_agency_costs, network_util

	def get_network_util_holism(self):

		network_cond_after = np.zeros((self.n_elements, self.n_steps))
		network_cond_before = np.zeros(self.n_elements).reshape(-1, 1)

		# Summation of the conditions of the condition ratings
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

		network_util_stepwise = np.zeros((self.n_elements, self.n_steps))
		# Converting the conditions to utility
		for element_idx, element in enumerate(self.network.assets[0].elements):
			network_util_stepwise[element_idx] = \
				element.utility_model.get(network_cond_before[element_idx], network_cond_after[element_idx])

		network_util_holism = np.sum(network_util_stepwise, axis = 1)
		network_util_holism = np.dot(self.network.assets[0].elements_util_weight, network_util_holism) * \
									self.network.n_assets
		return network_util_holism

	def get_network_stepwise(self):

		network_user_costs = np.zeros(self.n_steps)
		network_agency_costs = np.zeros(self.n_steps)
		network_util = np.zeros(self.n_steps)

		for asset in self.network.assets:
			
			network_user_costs += asset.accumulator.user_costs.get_stepwise()
			network_agency_costs += asset.accumulator.agency_costs.get_stepwise()
			network_util += asset.accumulator.asset_utils.get_stepwise()

		return network_user_costs, network_agency_costs, network_util

	def get_year_0(self):

		# Since there is a slight possibility that an earthquake happens in the year = 0, we do it 2 times and choose the minimum
		# In this way, it is almot impossible to see earthquakes in both of samplings

		year0_user_costs, year0_agency_costs, year0_utils = 0, 0, 0

		for asset in self.network.assets:

			# To make sure the accumulator does not contatin previous results
			asset.accumulator.refresh()

			user_costs_stepwise_1, elements_costs_stepwise_1, elements_utils_stepwise_1, elements_conds_stepwise1 = \
				self.simulator.get_one_instance(asset, random = self.random)
			user_costs_stepwise_2, elements_costs_stepwise_2, elements_utils_stepwise_2, elements_conds_stepwise2 = \
				self.simulator.get_one_instance(asset, random = self.random)

			asset.accumulator.update(user_costs_stepwise_1,
									elements_costs_stepwise_1,
									elements_utils_stepwise_1,
									elements_conds_stepwise1)

			year0_user_costs += min(user_costs_stepwise_1[0], user_costs_stepwise_2[0])
			year0_agency_costs += asset.accumulator.agency_costs.at_year(0)
			year0_utils = asset.accumulator.asset_utils.at_year(0)

		return year0_user_costs, year0_agency_costs, year0_utils

	def log_results(self):

		# Logging each asset independently
		print ("Logging the results")
		self.log.info(f"The results of the life cycle analysis: {self.lca_name}")

		for asset in self.network.assets:
			asset.accumulator.log_results(self.log, self.directory)
			self.log.info(f"MRR: {asset.mrr_model.mrr_to_decimal()}")

		# Logginf the network
		N = self.network.assets[0].accumulator.user_costs.simulator_counter

		user_costs = np.zeros(N)
		agency_costs = np.zeros(N)
		network_utils = np.zeros(N)

		for asset in self.network.assets:
			user_costs += asset.accumulator.user_costs.get_samples()
			agency_costs += asset.accumulator.agency_costs.get_samples()
			network_utils += asset.accumulator.asset_utils.get_samples()

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




	