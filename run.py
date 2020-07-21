import time


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
	
	mynetwork = IndianaNetwork("INDIANA2019")
	mynetwork.load_network(n_assets = 1)

	mynetwork.assets[0].mrr_model.set_mrr(np.array([[1,1,1,1,1,0,0,0,1,0,1,0], [1,0,1,0,1,0,1,0,1,0,1,1], [0,0,0,0,1,1,0,0,0,1,1,1]]))
	mynetwork.set_current_budget_limit(200)
	mynetwork.set_budget_limit_model(Linear(X0 = 200, drift = 0))
	mynetwork.set_npv_budget_limit(400)
	
	simulator = BridgeSimulator()
	
	lca = LCA(network = mynetwork,
			lca_name = session_name,
			simulator = simulator,
			random = False,
			is_hazard = True)

	return lca


def GA_test(obj):

	optimizer = GA(obj)
	optimizer.set_ga_chars(crossver_prob = 0.75,
							mutation_prob = 0.02,
							population_size = 100,
							n_generations = 200,
							n_elites = 5,
							optimzition_type = 'max',
							n_jobs = -1)
	optimizer.optimize()

def IUC_test(obj):

	optimizer = IUC(obj)
	optimizer.optimize()


if __name__ == "__main__":

	# GA_test(lca)

	# IUC_test()


	my_lca = lca()
	import matplotlib.pyplot as plt

	sim_utils = []

	# plt.ion()
	# for i in range(1000):

	# 	my_lca.run(1000)
	# 	sim_utils.append(my_lca.get_network_npv()[2])

	# 	plt.clf()
	# 	plt.xlabel('Simulations')
	# 	plt.ylabel('Utility')
		
	# 	plt.plot([i for i in range(len(sim_utils))], sim_utils)
		
	# 	plt.legend()
	# 	plt.grid(True, which = 'both')
	# 	plt.draw()
	# 	plt.pause(0.00001)

	start = time.time()
	my_lca.run(100000)
	print (time.time()-start)
	
	print (my_lca.get_network_npv())

	my_lca.log_results()

