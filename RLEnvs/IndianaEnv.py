#Loading dependencies
import time
import numpy as np

from .BaseEnv import BaseEnv

from Network import IndianaNetwork
from LifeCycleAnalyzer.Simulators import EnvSimulator
from utils.PredictiveModels import Linear, Power
from utils.NPV import NPV

class IndianaEnv(BaseEnv):

	def __init__(self, **params):
		super().__init__(**params)

		self.n_assets = params.pop("n_assets")
		self.loaded = False
		self._load_network()
		self.reset()

	def _load_network(self):

		# Creating the network
		session_name = 'IndianaEnv'
		self.network = IndianaNetwork(file_name = "INDIANA2019",
									settings = self.settings,
									n_assets = self.n_assets,
									is_deck = True,
					                is_superstructure = True,
					                is_substructure = True)
		self.network.load_network()
		self.reset_network_budget()
		self.asset_IDs = [asset.ID for asset in self.network.assets]

	def reset_network_budget(self):

		self.network.set_current_budget_limit(10000)
		self.network.set_annual_budget_limit_model(Power(X0 = 10000,
												growth_rate = 0.03,
												settings = self.settings))
		self.network.set_npv_budget_limit(10000)


		self.remaining_npv_budget = self.network.npv_budget_limit
		self.annual_budget_limit = self.network.annual_budget_model.predict_series()

	def reset(self):
		self.simulators = {}
		s_a_rs = {}
		
		self.reset_network_budget()


		for asset in self.network.assets:

			self.simulators[asset.ID] = EnvSimulator(asset = asset,
													settings = self.settings,
													random = True)
			s_a_rs[asset.ID] = self.simulators[asset.ID].reset()

			# Adding the remaining budget
			s_a_rs[asset.ID]['remaining_budget'] = self.remaining_npv_budget / self.network.npv_budget_limit

		return s_a_rs

	def enough_NPV_budget(self, actions):
		total_costs = 0

		for asset in self.network.assets:
			costs, _, _, step = self.simulators[asset.ID].cost_of(actions[asset.ID])
			total_costs += np.sum(costs) * \
							 np.exp(-self.settings.discount_rate * self.settings.dt * step)

		return total_costs <= self.remaining_npv_budget

	def enough_annual_budget(self, actions, step):
		total_costs = 0

		for asset in self.network.assets:
			costs, _, _, step = self.simulators[asset.ID].cost_of(actions[asset.ID])
			total_costs += np.sum(costs)

		return total_costs <= self.annual_budget_limit[step]


	def _deduct_npv_budget(self, s_a_rs):
		total_costs = 0
		for id_ in s_a_rs:

			npv_costs = np.sum(s_a_rs[id_]['elements_costs']) * \
							np.exp(-self.settings.discount_rate * self.settings.dt * (s_a_rs[id_]['step']-1))
			total_costs += npv_costs

		# This will never be less than zero because the enough_budget MUST be checked before it
		if total_costs < self.remaining_npv_budget:
			self.remaining_npv_budget -= total_costs
		else:
			self.remaining_npv_budget = -self.network.npv_budget_limit

		# self.remaining_npv_budget = max(self.remaining_npv_budget - total_costs, 0)

	def step(self, actions):
		'''Simulation for all assets in a network

		actions: a dictionary with key:asset_id, val: actions
		'''
		s_a_rs = {}

		for asset in self.network.assets:
			s_a_rs[asset.ID] = self.simulators[asset.ID].take_one_step(actions[asset.ID], is_hazard = True)

		# Let's deduct the budget
		self._deduct_npv_budget(s_a_rs)

		# Adding feature based on network information
		for asset in self.network.assets:
			s_a_rs[asset.ID]['remaining_budget'] = self.remaining_npv_budget / self.network.npv_budget_limit


		return s_a_rs