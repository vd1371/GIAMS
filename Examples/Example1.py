# -------------------------------------------------------------------- #
# This example was designed to show the project-level optimization
# option in GIAMS. This example was used in the original paper as well
# -------------------------------------------------------------------- #


import time
import ast

from Network.IndianaNetwork import IndianaNetwork
from LifeCycleAnalyzer.Simulators.BridgeSimulator import BridgeSimulator
from LifeCycleAnalyzer.LCA import LCA

from Optimizer.GA import GA
from Optimizer.IUC import IUC

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *


def lca():

	session_name = 'Indiana'
	
	mynetwork = IndianaNetwork("INDIANA2019", n_assets = 1)
	mynetwork.load_network()

	# The old one with 42
	mrr_str = "[[1 1 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 1] [0 1 0 1 0 0 0 1 0 0 1 0 0 0 0 1 1 0 0 0 0 1] [0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0]]"
	mrr_str = np.array(ast.literal_eval(mrr_str.replace(" ", ",")))
	mynetwork.assets[0].mrr_model.set_mrr(mrr_str)

	mynetwork.set_current_budget_limit(100000)
	mynetwork.set_budget_limit_model(Linear(X0 = 100000, drift = 0))
	mynetwork.set_npv_budget_limit(10000)

	simulator = BridgeSimulator()
	lca = LCA(network = mynetwork,
			lca_name = session_name,
			simulator = simulator,
			random = False,
			is_hazard = False,
			n_simulations = 2000)

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


def example1():

	# GA_test(lca)

	mylca = lca()
	# print (mylca.network.assets[0].mrr_model.mrr)

	# import matplotlib.pyplot as plt
	# all_utils = []
	# plt.ion()
	# for _ in range (100):

	# 	mylca.run()
	# 	_, _, new_util = mylca.get_network_npv()
	# 	all_utils.append(new_util)

	# 	plt.clf()
	# 	plt.plot([i for i in range(len(all_utils))], all_utils)
	# 	plt.legend()
	# 	plt.grid(True, which = 'both')
	# 	plt.draw()
	# 	plt.pause(0.00001)

	start = time.time()
	mylca.run(verbose = False)
	print (time.time() - start)
	print (mylca.get_network_npv())



if __name__ == "__main__":

	example1()




