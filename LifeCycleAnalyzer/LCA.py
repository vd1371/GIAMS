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
						logger = None,
						directory = None,
						log_level = logging.DEBUG):
		super().__init__(network, lca_name, simulator, logger, directory, log_level)

	def run(self, n_simulations = None):

		N = self.n_simulations if n_simulations is None else n_simulations

		for asset in self.network.assets:

			# Making sure that there is nothing in the memory
			asset.refresh()
			
			for i in range(N):

				other_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise = self.simulator.get_one_instance(asset)
				asset.accumulator.update(other_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise)

	def run_for_one_asset(self, asset, n_simulations = None):
		N = self.n_simulations if n_simulations is None else n_simulations

		asset.accumulator.refresh()
		for i in range(N):
			asset.refresh()
			other_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise = self.simulator.get_one_instance(asset, is_hazard= False)
			asset.accumulator.update(other_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise)

	def get_network_npv(self):
		
		network_other_costs = 0
		network_agency_costs = 0
		network_util = 0

		for asset in self.network.assets:

			network_other_costs += asset.accumulator.other_costs.expected()[0]
			network_agency_costs += asset.accumulator.agency_costs.expected()[0]
			network_util += asset.accumulator.asset_utils.expected()[0]

		return network_other_costs, network_agency_costs, network_util

	def get_network_stepwise(self):

		network_other_costs = np.zeros(self.n_steps)
		network_agency_costs = np.zeros(self.n_steps)
		network_util = np.zeros(self.n_steps)

		for asset in self.network.assets:
			network_other_costs += asset.accumulator.other_costs.get_stepwise()
			network_agency_costs += asset.accumulator.agency_costs.get_stepwise()
			network_util += asset.accumulator.asset_utils.get_stepwise()

		return network_other_costs, network_agency_costs, network_util

	def get_year_0(self):

		# Since there is a slight possibility that an earthquake happens in the year = 0, we do it 2 times and choose the minimum
		# In this way, it is almot impossible to see earthquakes in both of samplings

		year0_other_costs, year0_agency_costs, year0_utils = 0, 0, 0

		for asset in self.network.assets:

			# To make sure the accumulator does not contatin previous results
			asset.accumulator.refresh()

			other_costs_stepwise_1, elements_costs_stepwise_1, elements_utils_stepwise_1 = self.simulator.get_one_instance(asset)
			other_costs_stepwise_2, elements_costs_stepwise_2, elements_utils_stepwise_2 = self.simulator.get_one_instance(asset)

			asset.accumulator.update(other_costs_stepwise_1, elements_costs_stepwise_1, elements_utils_stepwise_1)

			year0_other_costs += min(other_costs_stepwise_1[0], other_costs_stepwise_2[0])
			year0_agency_costs += asset.accumulator.agency_costs.at_year(0)
			year0_utils = asset.accumulator.asset_utils.at_year(0)

		return year0_other_costs, year0_agency_costs, year0_utils

	def log_results(self):

		# Logging each asset independently
		print ("Logging the results")
		self.log.info(f"The results of the life cycle analysis: {self.lca_name}")

		for asset in self.network.assets:
			asset.accumulator.log_results(self.log, self.directory)
			self.log.info(f"MRR: {asset.mrr_model.mrr_to_decimal()}")

		# Logginf the network
		other_costs = np.zeros(self.n_simulations)
		agency_costs = np.zeros(self.n_simulations)
		network_utils = np.zeros(self.n_simulations)

		for asset in self.network.assets:
			other_costs += asset.accumulator.other_costs.get_samples()
			agency_costs += asset.accumulator.agency_costs.get_samples()
			network_utils += asset.accumulator.asset_utils.get_samples()

		self.log.info(f"The network other costs Mean: {round(np.mean(other_costs),2)} , Stdv:{round(np.std(other_costs),2)}")
		self.log.info(f"The network agency costs Mean: {round(np.mean(agency_costs),2)} , Stdv:{round(np.std(agency_costs),2)}")
		self.log.info(f"The network utils Mean: {round(np.mean(network_utils),2)} , Stdv:{round(np.std(network_utils),2)}")

		year0_other_costs, year0_agency_costs, year0_utils  =self.get_year_0()

		self.log.info(f"At year 0 - other costs: {year0_other_costs:.2f}, agency costs : {year0_agency_costs}, util: {year0_utils:.2f}")

		plt.clf()
		plt.hist(other_costs)
		plt.savefig(self.directory + f"/OtherCostHistogram.png")

		plt.clf()
		plt.hist(agency_costs)
		plt.savefig(self.directory + f"/AgencyCostHistogram.png")

		plt.clf()
		plt.hist(network_utils)
		plt.savefig(self.directory + f"/Network-UtilsHistogram.png")

	

	def get_objective1(self):
		return self.network.objective1()

	def get_objective2(self):
		return self.network.objective2()




	