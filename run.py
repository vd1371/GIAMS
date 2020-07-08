import time


from Network.FirstNetwork import FirstNetwork
from LifeCycleAnalyzer.Simulators.BridgeSimulator import BridgeSimulator
from LifeCycleAnalyzer.LCA import LCA

from Optimizer.GA import GA
from Optimizer.IUC import IUC

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *

def lca():

	session_name = 'Test'
	
	mynetwork = FirstNetwork("FirstNetwork")
	mynetwork.load_network(n_assets = 3)

	# mynetwork.assets[0].mrr_model.set_mrr([[0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1], [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0]])
	mynetwork.set_current_budget_limit(20)
	mynetwork.set_budget_limit_model(Linear(X0 = 20, drift = 2))
	mynetwork.set_npv_budget_limit(80)
	
	simulator = BridgeSimulator()
	
	lca = LCA(network = mynetwork,
			lca_name = session_name,
			simulator = simulator)

	return lca


def GA_test():
	obj = lca()

	optimizer = GA(obj)
	optimizer.set_ga_chars(crossver_prob = 0.75,
							mutation_prob = 0.02,
							population_size = 10,
							n_generations = 10,
							n_elites = 5,
							optimzition_type = 'max')
	optimizer.optimize()

def IUC_test():

	obj = lca()

	optimizer = IUC(obj)

	optimizer.optimize()



if __name__ == "__main__":

	# GA_test()

	IUC_test()

	# my_lca = lca()
	# my_lca.run()
	# my_lca.log_results()

