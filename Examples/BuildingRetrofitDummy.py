# -------------------------------------------------------------------- #
# This example was designed to show the usefulness of GIAMS in another example
# in the original paper
# -------------------------------------------------------------------- #


import time
import ast

from Network.DummyBuildingNetwork import BuildingNetwork
from LifeCycleAnalyzer.Simulators.MainSimulator import MainSimulator
from LifeCycleAnalyzer.LCA import LCA

from Optimizer.GA import GA
from Optimizer.IUC import IUC

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *


def lca():

	session_name = 'BuildingRetrofit'
	
	mynetwork = BuildingNetwork(None, n_assets = 1)
	mynetwork.load_network()

	# The old one with 42
	# mrr_str = "[[1 1 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0] [0 1 0 1 0 0 0 1 0 0 1 0 0 0 0 1 1 0 0 0] [0 1 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0]]"
	# mrr_str = np.array(ast.literal_eval(mrr_str.replace(" ", ",")))
	# mynetwork.assets[0].mrr_model.set_mrr(mrr_str)

	mynetwork.set_current_budget_limit(100000)
	mynetwork.set_budget_limit_model(Linear(X0 = 100000, drift = 0))
	mynetwork.set_npv_budget_limit(10000)

	simulator = MainSimulator()
	lca = LCA(network = mynetwork,
			lca_name = session_name,
			simulator = simulator,
			random = False,
			is_hazard = False,
			n_simulations = 20)

	return lca


def GA_test(obj):

	optimizer = GA(obj)
	optimizer.set_ga_chars(crossver_prob = 0.75,
							mutation_prob = 0.03,
							population_size = 200,
							n_generations = 100,
							n_elites = 5,
							optimzition_type = 'max',
							n_jobs = -1)
	optimizer.optimize()


def example():

	mylca = lca()

	start = time.time()
	mylca.run(verbose = False)
	print (time.time() - start)
	print (mylca.get_network_npv())



if __name__ == "__main__":

	example1()




