# -------------------------------------------------------------------- #
# This example was designed to show the project-level optimization
# option in GIAMS. This example was used in the original paper as well
# -------------------------------------------------------------------- #


import time
import ast

from Network import IndianaNetwork
from LifeCycleAnalyzer.Simulators import MainSimulator
from LifeCycleAnalyzer import LCA

from Optimizer import GA
from Optimizer import IUC

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *

class GeneralSettings:

	n_elements = 1
	n_states = 8
	dt = 1
	horizon = 50
	discount_rate = 0.03

	init_year = 0
	n_steps = int(horizon/dt)
	
	DONOT = 0
	MAINT = 1
	REHAB = 2
	RECON = 3
	BINAR = 1


def lca_instance():

	# Creating the network
	session_name = 'Indiana'
	mynetwork = IndianaNetwork("INDIANA2019",
								n_assets = 1,
								is_deck = True,
				                is_superstructure = True,
				                is_substructure = True)
	mynetwork.load_network()
	mynetwork.set_current_budget_limit(100000)
	mynetwork.set_budget_limit_model(Linear(X0 = 100000, drift = 0))
	mynetwork.set_npv_budget_limit(10000)

	# Creating the simulator
	simulator = MainSimulator()

	# Creating the settings instance
	settings = GeneralSettings()

	# shaping the main LCA
	lca = LCA(lca_name = session_name,
			settings = settings,
			network = mynetwork,
			simulator = simulator,
			random = True,
			is_hazard = True,
			n_simulations = 10)

	return lca

def obj_func(**kwargs):
		return kwargs['Utility'] / kwargs['UserCost'] ** 0.2

def GA_test(obj):

	optimizer = GA(obj)
	optimizer.set_ga_chars(crossver_prob = 0.75,
							mutation_prob = 0.03,
							population_size = 20,
							n_generations = 10,
							n_elites = 5,
							optimzition_type = 'max',
							n_jobs = -1)
	
	optimizer.set_obj_func(obj_func)

	optimizer.optimize()


def example1():

	# GA_test(lca)

	mylca = lca_instance()
	start = time.time()
	mylca.run(verbose = False)
	print (time.time() - start)
	print (mylca.get_network_npv())



if __name__ == "__main__":

	example1()
	GA_test(lca_instance)




