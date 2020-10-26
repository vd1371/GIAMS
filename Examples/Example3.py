# -------------------------------------------------------------------- #
# This eexample was designed to show the GA can produce near optimal solutions
# It was used as a response to reviewers of AUTCON journal
# -------------------------------------------------------------------- #


import time
import ast

import pandas as pd
import multiprocessing as mp
from multiprocessing import Process, Queue
import itertools

from Network.IndianaNetwork import IndianaNetwork
from LifeCycleAnalyzer.Simulators.BridgeSimulator import BridgeSimulator
from LifeCycleAnalyzer.LCA import LCA

from Optimizer.GA import GA
from Optimizer.IUC import IUC

from utils.PredictiveModels.Linear import Linear
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *


def lca(mrr = None):

	session_name = 'Indiana'
	
	mynetwork = IndianaNetwork("INDIANA2019",
								n_assets = 1,
								is_deck = False,
				                is_superstructure = True,
				                is_substructure = False)
	mynetwork.load_network()

	if not mrr is None:
		mynetwork.assets[0].mrr_model.set_mrr(mrr)

	mynetwork.set_current_budget_limit(100000)
	mynetwork.set_budget_limit_model(Linear(X0 = 100000, drift = 0))
	mynetwork.set_npv_budget_limit(10000)

	simulator = BridgeSimulator()
	lca = LCA(network = mynetwork,
			lca_name = session_name,
			simulator = simulator,
			random = False,
			is_hazard = False,
			n_simulations = 500)

	return lca


def GA_test(obj):

	optimizer = GA(obj)
	optimizer.set_ga_chars(crossver_prob = 0.75,
							mutation_prob = 0.1,
							population_size = 50,
							n_generations = 100,
							n_elites = 5,
							optimzition_type = 'max',
							n_jobs = -1)
	optimizer.optimize()

@timeit
def example():

	mylca = lca()
	mylca.run()
	# GA_test(lca)

# ---------------------------- #
# For the parallel section     #
def lca_for_validation(mrrs, q_out):
	session_name = 'Indiana'
	mynetwork = IndianaNetwork("INDIANA2019",
								n_assets = 1,
								is_deck = False,
				                is_superstructure = True,
				                is_substructure = False)
	mynetwork.load_network()
	mynetwork.set_current_budget_limit(100000)
	mynetwork.set_budget_limit_model(Linear(X0 = 100000, drift = 0))
	mynetwork.set_npv_budget_limit(10000)

	for mrr in mrrs:
		mynetwork.assets[0].mrr_model.set_mrr(np.atleast_2d(mrr))

		simulator = BridgeSimulator()
		lca = LCA(network = mynetwork,
				lca_name = session_name,
				simulator = simulator,
				random = False,
				is_hazard = False,
				n_simulations = 1000)
		
		lca.run()
		results = lca.get_network_npv()

		q_out.put(mrr + results)


def validate_ga(N = None):

	results_queue = Queue()
	n_cores = mp.cpu_count()-2

	genset = GenSet()
	combs = list(itertools.product([0, 1], repeat = genset.n_steps * genset.dt * genset.n_elements))
	if not N is None:
		combs = combs[:N]

	slicer = int(len(combs)/n_cores) + 1

	# Creating and filling the pool
	pool = []
	for j in range (n_cores):
		init_idx = j * slicer
		last_idx = (j + 1) * slicer if j < n_cores-1 else len(combs)
		worker = Process(target = lca_for_validation, args = (combs[init_idx: last_idx], results_queue,))
		pool.append(worker)

	print('starting processes...')
	for worker in pool:
		worker.start()

	all_samples = []
	done_workers = 0
	batch_number = 0

	while any(worker.is_alive() for worker in pool):

		while not results_queue.empty():

			sample = results_queue.get()

			if not sample is None:
				all_samples.append(sample)

	print('waiting for workers to join...')
	for worker in pool:
		worker.join()
	print('all workers are joined.\n')

	cols = []
	for elem_number in range(genset.n_elements):
		for i in range (genset.dt*genset.n_steps):
			cols.append(f'Eelem{elem_number}-{i}')
	cols += ['UserCost', 'AgencyCost', 'Utility']

	df = pd.DataFrame(all_samples, columns = cols)

	df.to_csv(f"./reports/GA-Validation.csv")
	print (f'Data is saved now')


if __name__ == "__main__":

	# example1()
	validate_ga()




