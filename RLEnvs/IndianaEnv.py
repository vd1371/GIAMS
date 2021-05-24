#Loading dependencies
import time
from copy import deepcopy

from .BaseEnv import BaseEnv

from Network import IndianaNetwork
from LifeCycleAnalyzer.Simulators import EnvSimulator
from utils.PredictiveModels.Linear import Linear

class IndianaEnv(BaseEnv):

	def __init__(self, **params):
		super().__init__(**params)

		self.simulator = EnvSimulator(**params)
		self.n_assets = params.pop("n_assets")

		self.network = self._load_network()
		self.asset_IDs = [asset.ID for asset in self.network.assets]

	def _load_network(self):

		# Creating the network
		session_name = 'IndianaEnv'
		network = IndianaNetwork(file_name = "INDIANA2019",
									settings = self.settings,
									n_assets = self.n_assets,
									is_deck = True,
					                is_superstructure = True,
					                is_substructure = True)
		network.load_network()

		network.set_current_budget_limit(10000)
		network.set_budget_limit_model(Linear(X0 = 10000,
												drift = 0,
												settings = self.settings))
		network.set_npv_budget_limit(20000)

		return network

	def reset(self):
		self.network = self._load_network()

	def go_one_lifecycle(self, models, eps):
		'''Simulation for all assets in a network '''

		# Holder for network state, actions, and rewards
		s_a_rs = {}

		for asset, model in zip(self.network.assets, models):

			s_a_r[asset.ID] = self.simulator.simulate(asset, model, eps)
		
		return s_a_r