# -------------------------------------------------------------------- #
# This example was designed to show the project-level optimization
# option in GIAMS. This example was used in the original paper as well
# -------------------------------------------------------------------- #


import time
import ast

from Network import IndianaNetwork
from LifeCycleAnalyzer.Simulators import MainSimulator
from LifeCycleAnalyzer import LCA

from Optimizer import HillClimbing
from Optimizer import BruteForce
from Optimizer import GA
from Optimizer import IUC
from Optimizer import PSO

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *

class GeneralSettings:

	n_elements = 3
	n_states = 8
	dt = 2
	horizon = 20
	discount_rate = 0.03
	init_year = 0
	n_steps = int(horizon/dt)


def lca_instance():

	# Creating the settings instance
	settings = GeneralSettings()

	# Creating the network
	session_name = 'IndianaTest'
	mynetwork = IndianaNetwork(file_name = "INDIANA2019",
								settings = settings,
								n_assets = 1,
								is_deck = True,
				                is_superstructure = True,
				                is_substructure = True)
	mynetwork.load_network()
	mynetwork.set_current_budget_limit(100000)
	mynetwork.set_budget_limit_model(Linear(X0 = 100000, drift = 0, settings = settings))
	mynetwork.set_npv_budget_limit(10000)

	# Creating the simulator
	simulator = MainSimulator(settings = settings)

	# shaping the main LCA
	lca = LCA(lca_name = session_name,
			settings = settings,
			network = mynetwork,
			simulator = simulator,
			random = True,
			is_hazard = True,
			n_simulations = 5,
			should_report = True)

	return lca

def obj_func(**kwargs):
		return kwargs['Utility'] / kwargs['UserCost'] ** 0.2

def GA_test():

	optimizer = GA(lca_instance)
	optimizer.set_hyperparameters(crossver_prob = 0.75,
							mutation_prob = 0.03,
							population_size = 200,
							n_generations = 200,
							n_elites = 5,
							optimzition_type = 'max',
							n_jobs = 1)

	optimizer.set_obj_func(obj_func)
	# optimizer.optimize(rounds = 3)
	optimizer.validate()

def hill_climbing():

	optimizer = HillClimbing(lca_instance)
	optimizer.set_hyperparameters(stochastic = False,
								optimzition_type = 'max',
								n_jobs = 1)
	optimizer.set_obj_func(obj_func)
	optimizer.optimize(rounds = 3,
						verbose = 1)

def brute_force():
	optimizer = BruteForce(lca = lca_instance)
	optimizer.set_hyperparameters(optimzition_type = 'max',
									n_jobs = 1)
	optimizer.set_obj_func(obj_func)
	optimizer.optimize(verbose = 1)

def pso():
	optimizer = PSO(lca_instance)
	optimizer.set_hyperparameters(n_particles = 200,
									k = 50,
									n_jobs = 1,
									iter = 10)
	optimizer.set_obj_func(obj_func)
	optimizer.optimize(verbose = 1)

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




