#Loading dependencies
import time
import numpy as np
import pandas as pd
import multiprocessing as mp
from multiprocessing import Queue, Process
from itertools import product
from ._Solution import Solution, _eval_sol

class BruteForce:

	def __init__(self, lca = None):

		# Objective_function is an instance of lca
		self.lca = lca

		# Gettign one instance the objective function
		self.lca_ref = lca()

		# lca has network, directory, log, and 
		self.directory = self.lca_ref.directory
		self.log = self.lca_ref.log

		asset_mrr_shape = self.lca_ref.network.assets[0].mrr_model.mrr.shape
		n_assets = len(self.lca_ref.network.assets)

		# It will be used to reshape the solution to 1d and original shape
		self.solut_shape = (n_assets, asset_mrr_shape[0], asset_mrr_shape[1])
		# It will be used for producing all combination of n binaries
		# It equals to number of assets x number of elements x number of decision making step
		# .. in the future
		self.binary_shape = n_assets * asset_mrr_shape[0] * asset_mrr_shape[1]

	def _solut_to_1d_shape(self, solut):
		return solut.reshape(-1)

	def _solut_to_original_shape(self, solut):
		return np.array(solut).reshape(self.solut_shape)

	def set_hyperparameters(self, **params):

		self.optimization_type = params.pop('optimzition_type', 'max')
		self.n_jobs = params.pop('n_jobs', 1)

		self.log.info((f"BruteForce is started. \n"
					f"Optimization type: {self.optimization_type} \n"
					f"n_jobs: {self.n_jobs} \n"
					))

		if self.optimization_type == 'min':
			self.sorting_order = False
		elif self.optimization_type == 'max':
			self.sorting_order = True

	def set_obj_func(self, obj_func):
		self.obj_func = obj_func

	def _possible_mrr(self, mrr_que):

		# Getting all possible combination of the binary array for MRR
		all_combinations = product([0, 1], repeat = self.binary_shape)

		for mrr in all_combinations:
			while mrr_que.qsize() > 100:
				pass

			if mrr_que.qsize() < 100:
				mrr_que.put(mrr)


	def optimize(self, verbose = 1):

		mrr_que = Queue()




		

		return

	def get_neighbours(self, ind):
		'''Finding neighbours of the solution'''
		print ("Trying to get new neighbours")
		neighbours = []
		old_solution = self._solut_to_1d_shape(ind.get_solut())

		if self.stochastic:
			while True:
				new_solution = np.copy(old_solution)
				idx = np.random.choice(range(len(new_solution)))
				new_solution[idx] = 0 if new_solution[idx] == 1 else 1

				# Checking if we have already seen this point
				if not self._is_in_taboo_list(old_solution):
					new_solution = self._solut_to_original_shape(new_solution)
					new_solution = Solution(lca = self.lca,
											solut = np.copy(new_solution),
											obj_func = self.obj_func)
					if new_solution.is_valid():
						neighbours.append(new_solution)
						break

		else:
			for idx in range(len(old_solution)):
				new_solution = np.copy(old_solution)
				new_solution[idx] = 0 if new_solution[idx] == 1 else 1

				if not self._is_in_taboo_list(new_solution):
					new_solution = self._solut_to_original_shape(new_solution)
					new_solution = Solution(lca = self.lca,
											solut = np.copy(new_solution),
											obj_func = self.obj_func)
					if new_solution.is_valid():
						neighbours.append(new_solution)

		return neighbours

	def get_best_neighbour(self, neighbours):
		'''Finding the best neighbour'''
		print ('Trying to analyze neighbours')
		n = len(neighbours)
		if self.n_jobs == 1:
			for i, ind in enumerate(neighbours):
				start = time.time()
				ind.evaluate()
				print (f"Ind {i}/{n} in {time.time()-start:.2f}")

		else:
			with mp.Pool(max(-self.n_jobs * mp.cpu_count(), self.n_jobs)) as P:
				to_be_eval = P.map(_eval_ind, neighbours)

		# Sorting the generation based on their value and the optimization type
		neighbours = sorted(neighbours, key=lambda x: x.value, reverse = self.sorting_order)
		# Returning the best neighbour
		return neighbours[0]





