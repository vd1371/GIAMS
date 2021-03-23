#Loading dependencies
import time
import numpy as np
import pandas as pd
import multiprocessing as mp
from multiprocessing import Queue, Process
from itertools import product
from ._objectives import LCASolution
from ._objectives import _eval_sol

class BruteForce:

	def __init__(self, **params):

		# Objective_function is an instance of lca
		lca = params.pop('lca')
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
		self.dimension = n_assets * asset_mrr_shape[0] * asset_mrr_shape[1]

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

	def _mrr_generator(self):
		'''Naive mrr generator for brute foce algorithm
		
		Future development: Develop a smarter one
		'''
		# Getting all possible combination of the binary array for MRR
		all_combinations = product([0, 1], repeat = self.dimension)

		for mrr in all_combinations:
			yield mrr

	def _possible_solution(self, solution_que):

		optimization_start = time.time()
		for i, mrr in enumerate(self._mrr_generator()):

			while solution_que.qsize() > 100:
				pass

			# Creating a new solution
			solut = self._solut_to_original_shape(mrr)
			new_sol = LCASolution(lca = self.lca,
								solut = solut,
								obj_func = self.lca_ref.network.objective)

			# printing the progress
			if i % 100 == 0:
				print (f"{i}/{2**self.dimension} solutions are suggested so far in "
						f"{time.time() - optimization_start:.2f} seconds")
			
			# Checking if the generated mrr is valid
			if new_sol.is_valid():
				solution_que.put(new_sol)

	def optimize_parallel(self, verbose = 1):

		# Queue for generated mrrs
		solution_que = Queue()
		solution_generator = Process(target = self._possible_solution, args = (solution_que,))
		solution_generator.start()

		# Creaing a pool of workers for analysis
		analysis_que = Queue()
		workers_pool = []
		for i in range(self.n_jobs - 1):
			worker = Process(target = _eval_sol_q, args = (solution_que, analysis_que,))
			worker.start()
			workers_pool.append(worker)
		print ("workers started analysis...")

		# Getting the results and saving them
		first = True
		start = time.time()
		while True:
			while not analysis_que.empty():
				solut = analysis_que.get()

				if first:
					best_solution = solut
					first = False
				else:
					if solut.value > best_solution.value:
						best_solution = solut
						if verbose == 1:
							print (f'A better solution is found\n{best_solution}')
						self.log.info(f"BruteForce: Best solution so far: {best_solution} \n")

				# To check the last time any analysis has been produced
				start = time.time()

			# If after a certain amount of time, there is nothing in the
			# ... analysis queue, then probably no more solutions will be
			# ... produced
			if time.time() - start > 120:
				ans = input('more than 2 minutes but no new results, terminate? (y/n) :')
				
				if ans.lower() == "y":
					break
				else:
					# Refresh time counter
					start = time.time() 

		# Joining all processes
		solution_generator.join()
		for worker in workers_pool:
			worker.join()
		print ("Done")

	def optimize_linear(self, verbose = 1):

		optimization_start = time.time()

		first = True
		for i, mrr in enumerate(self._mrr_generator()):

			if i % 100 == 0:
				print (f"{i}/{2**self.dimension} solutions are analyzed so far in "
						f"{time.time() - optimization_start:.2f} seconds")

			# Creating a new solution
			solut = self._solut_to_original_shape(mrr)
			solut = LCASolution(lca = self.lca,
								solut = solut,
								obj_func = self.lca_ref.network.objective)
			
			# Checking if the generated mrr is valid
			if solut.is_valid():
				# To keep track of the time of the last valid solution
				start = time.time()
				# Evaluate the solution
				solut.evaluate()

				if first:
					best_solution = solut
					first = False
				else:
					if solut.value > best_solution.value:
						best_solution = solut
						if verbose == 1:
							print (f'A better solution is found\n{best_solution}')
						self.log.info(f"BruteForce: Best solution so far: {best_solution} \n")

			if time.time() - start > 120:
				ans = input('more than 2 minutes but no new results, terminate? (y/n) :')
				
				if ans.lower() == "y":
					break
				else:
					# Refresh time counter
					start = time.time()
		print ("Done")

	def optimize(self, verbose = 1):
		'''Conducting the optimization'''
		if self.n_jobs == 1:
			self.optimize_linear(verbose = verbose)

		else:
			self.optimize_parallel(verbose = verbose)

def _eval_sol_q(solution_que, analysis_que):
	'''Producer_consumer function

	solution queue: a queue of possible solutions
	analysis queue: a qeueu of analyzed solutions
	'''
	while True:
		while not solution_que.empty():
			solut = solution_que.get()
			solut.evaluate()
			analysis_que.put(solut)



