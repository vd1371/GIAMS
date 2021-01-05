# -------------------------------------------------------------------- #
# This example was designed to show the usefulness of GIAMS in another example
# in the original paper
# -------------------------------------------------------------------- #


import time
import ast

from Network.DummyBuildingNetwork import BuildingNetwork
from LifeCycleAnalyzer.Simulators.DummyRiskAnalyzer import DummyRiskAnalyzer
from LifeCycleAnalyzer.LCA import LCA

from Optimizer.Rank import Rank

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *


def lca():

	session_name = 'BuildingRetrofit'
	
	mynetwork = BuildingNetwork(None, n_assets = 5)
	mynetwork.load_network()

	mynetwork.set_current_budget_limit(100000)
	mynetwork.set_budget_limit_model(Linear(X0 = 100000, drift = 0))
	mynetwork.set_npv_budget_limit(10000)

	simulator = DummyRiskAnalyzer()
	lca = LCA(network = mynetwork,
			lca_name = session_name,
			simulator = simulator,
			random = False,
			is_hazard = False,
			n_simulations = 1)

	return lca

def example():

	start = time.time()
	opt = Rank(lca)
	print (opt.optimize())



if __name__ == "__main__":

	example()




