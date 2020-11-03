# -------------------------------------------------------------------- #
# This is the main code of the EstLCA paper
# -------------------------------------------------------------------- #


import time
import ast

import pandas as pd
import multiprocessing as mp
from multiprocessing import Process, Queue

from Network.RandomNetwork import RandomNetwork
from LifeCycleAnalyzer.Simulators.BridgeSimulator import BridgeSimulator
from LifeCycleAnalyzer.LCA import LCA

from utils.PredictiveModels.Linear import Linear
from utils.PredictiveModels.WienerDrift import WienerDrift
from utils.AwesomeTimeIt import timeit
from utils.GeneralSettings import *

def EstLca():

	session_name = 'EstLca'
	
	mynetwork = RandomNetwork(file_name = None, n_assets = 1)
	
	params = mynetwork.load_network()
	mrr = mynetwork.assets[0].mrr_model.mrr

	# The old one with 42
	# mrr_str = "[[1 1 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 1] [0 1 0 1 0 0 0 1 0 0 1 0 0 0 0 1 1 0 0 0 0 1] [0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0]]"
	# mrr_str = np.array(ast.literal_eval(mrr_str.replace(" ", ",")))
	# mynetwork.assets[0].mrr_model.set_mrr(mrr_str)

	simulator = BridgeSimulator()
	lca = LCA(network = mynetwork,
			lca_name = session_name,
			simulator = simulator,
			random = True,
			is_hazard = True,
			n_simulations = 1000,
			should_report = False)

	try:
		lca.run(verbose = False)
		results = lca.get_network_npv()

		output = list(params.values())
		output += list(mrr.reshape(1, -1).tolist()[0])
		for val in results:
			output.append(val)

		return output

	except ValueError:
		return None


def run_EstLca(N, que):
	for i in range(N):
		que.put(EstLca())


def run_parallel(N = 1000, batch_size = 200):

	results_queue = Queue()
	n_cores = mp.cpu_count()-2
	N_for_core = int(N/n_cores)

	# Creating columns for the output datafram
	cols = ['id', 'length', 'width', 'material', 'design', 'vertical_clearance', 'road_class', 'ADT', 
			'truck_percentage', 'detour_length', 'hazus_class', 'site_class', 'skew_angle', 'n_spans', 
			'maint_duration', 'rehab_duration', 'recon_duration', 'speed_before', 'speed_after', 'drift',
			'volatility', 'detour_usage_percentage', 'occurrence_rate', 'dist_first_param',
			'dist_second_param', 'deck_cond', 'deck_age', 'deck_material', 'superstructure_cond',
			'superstructure_age', 'substructure_cond', 'substructure_age']

	genset = GenSet()
	for elem_number in range(genset.n_elements):
		for i in range (2*genset.n_steps):
			cols.append(f'Eelem{elem_number}-{i}')

	cols += ['UserCost', 'AgencyCost', 'Utility']

	# Creating and filling the pool
	pool = []
	for j in range (n_cores):
		worker = Process(target = run_EstLca, args = (N_for_core, results_queue,))
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

		if len(all_samples) > batch_size:
			
			batch_number += 1

			df = pd.DataFrame(all_samples[:batch_size], columns = cols)
			df.to_csv(f"./reports/EstLca-{batch_number}.csv")
			
			print (f'Batch number {batch_number} is done')
			all_samples = all_samples[batch_size:]

	if len(all_samples) > 0:
		batch_number += 1
		df = pd.DataFrame(all_samples, columns = cols)
		df.to_csv(f"./reports/EstLca-{batch_number}.csv")
		print (f'Batch number {batch_number} is done')

	print('waiting for workers to join...')
	for worker in pool:
		worker.join()
	print('all workers are joined.\n')


if __name__ == "__main__":

	EstLca()

	start = time.time()

	run_parallel(N = 1000, batch_size = 200)

	print (f"It took {time.time()-start:.2f}")
	





