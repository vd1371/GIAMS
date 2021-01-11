import time
import numpy as np
import pandas as pd
from deap import tools
import matplotlib.pyplot as plt

import multiprocessing as mp
import ast

class Individual:

	def __init__(self, lca, chrom = None, val = None, flag = 'Regular', obj_func = None):

		self.lca_instance = lca()
		self.lca_instance.network.set_network_mrr(chrom)
		self.chrom = chrom
		self.value = val
		self.flag = flag
		self.obj_func = obj_func
		self.hash_ = hash(self.chrom.tostring())

	def evaluate(self):

		self.lca_instance.run()
		if self.lca_instance.check_budget():
			user_costs, agency_costs, utilities = self.lca_instance.get_network_npv()
			self.value = self.obj_func (UserCost = user_costs,
										AgencyCost = agency_costs,
										Utility = utilities)
		else:
			self.value = -1000

	def is_valid(self):

		for asset in self.lca_instance.network.assets:
			if not asset.mrr_model.check_policy():
				# To check whether the mrr meets certain policies
				# For example only two reconstrcution for an element in the horizon
				return False
		return True

	def set_value(self, val):
		self.value = val

	def set_chrom(self, chrom):
		self.chrom = chrom

	def get_chrom(self):
		return np.copy(self.chrom)

	def __repr__(self):
		return f"Ind {self.flag} - {self.hash_} - {self.chrom} - Val:{self.value}"
	
	def __str__(self):
		return f"Ind {self.flag} - {self.hash_} - {self.chrom} - Val:{self.value}"

# Creating a local function for to evaluate the individuals
def _eval_ind(ind):
	ind.evaluate()
	return ind

class HillClimbing:

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

		# It will be used to reshape the chromosome to 1d and original shape
		self.chrom_shape = (n_assets, asset_mrr_shape[0], asset_mrr_shape[1])

		# To prevent double checking the checked individuals
		self.taboo_list = []

	def _add_to_taboo_list(self, chrom):
		self.taboo_list.append(hash(chrom.tostring()))

	def _is_in_taboo_list(self, chrom):
		return hash(chrom.tostring()) in self.taboo_list

	def _chrom_to_1d_shape(self, chrom):
		return chrom.reshape(-1)

	def _chrom_to_original_shape(self, chrom):
		return np.array(chrom).reshape(self.chrom_shape)

	def set_hyperparameters(self, **params):

		self.stochastic = params.pop('stochastic')
		self.optimization_type = params.pop('optimzition_type', 'max')
		self.n_neighbours = params.pop('n_neighbours', 10)
		self.mutation_prob = params.pop('mutation_prob', 0.03)
		self.n_jobs = params.pop('n_jobs', 1)

		self.log.info((f"Hill Climbing optimization is started. \n"
					f"Stochastic: {self.stochastic} \n"
					f"Optimization type: {self.optimization_type} \n"
					f"n_jobs: {self.n_jobs} \n"
					))

		if self.optimization_type == 'min':
			self.sorting_order = False
		elif self.optimization_type == 'max':
			self.sorting_order = True

	def set_obj_func(self, obj_func):
		self.obj_func = obj_func

	def random_solution(self):
		'''Randomly find a solution

		The proportion of 1 in the initial chrom would be [0.1, 0.2, 0.3, 0.4, 0.5]
		Higher probabilities would lead to higher costs, therefore, 0.5 would be the biggest proportion
		'''
		while True:
			p = np.random.choice([0.1, 0.2, 0.3, 0.4, 0.5])
			chrom = np.random.choice([0,1], size = self.chrom_shape, p = [1-p, p])
			new_solution = Individual(self.lca, chrom = chrom, obj_func = self.obj_func)
			if new_solution.is_valid():
				new_solution.evaluate()
				self._add_to_taboo_list(chrom)
				return new_solution

	def get_neighbours(self, ind):
		'''Finding neighbours of the solution'''
		print ("Trying to get new neighbours")
		neighbours = []
		old_solution = self._chrom_to_1d_shape(ind.get_chrom())

		if self.stochastic:
			while True:
				new_solution = np.copy(old_solution)
				idx = np.random.choice(range(len(new_solution)))
				new_solution[idx] = 0 if new_solution[idx] == 1 else 1

				# Checking if we have already seen this point
				if not self._is_in_taboo_list(old_solution):
					new_solution = self._chrom_to_original_shape(new_solution)
					new_solution = Individual(self.lca, np.copy(new_solution), obj_func = self.obj_func)
					if new_solution.is_valid():
						neighbours.append(new_solution)
						break

		else:
			for idx in range(len(old_solution)):
				new_solution = np.copy(old_solution)
				new_solution[idx] = 0 if new_solution[idx] == 1 else 1

				if not self._is_in_taboo_list(new_solution):
					new_solution = self._chrom_to_original_shape(new_solution)
					new_solution = Individual(self.lca, np.copy(new_solution), obj_func = self.obj_func)
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

	def optimize(self,
				should_plot = True,
				should_plot_live = False,
				rounds = 1):

		best_values = []
		step = 0
		i = 0
		start = time.time()
		while True:

			# Geenrating a random soluton for initalization of the optimization
			if step == 0:
				current_solution = self.random_solution()

			# Getting the neighbours and the best neighbour
			neighbours = self.get_neighbours(current_solution)
			best_neighbour = self.get_best_neighbour(neighbours)

			# For maximization
			if best_neighbour.value > current_solution.value:
				current_solution = best_neighbour
				best_values.append(max(best_neighbour.value, 0))

				log_str = "\n"
				log_str += f"Round {i} - Step: {step} - {best_neighbour} - "\
								f"TabooListLength: {len(self.taboo_list)} \n"
				print (f"Round {i} - Step: {step} - {best_neighbour} "\
							f"TabooListLength: {len(self.taboo_list)} - "\
							f"Timme elapsed: {time.time()-start:.2f}")

				# Plotting the value online
				if should_plot_live:
					plt.ion()
					plt.clf()
					plt.title(f'Step {step}')
					plt.xlabel('Step')
					plt.ylabel('Objective value')
					
					plt.plot([i for i in range(len(best_values))], best_values, label="Best individual")
					
					plt.legend()
					plt.grid(True, which = 'both')
					plt.draw()
					plt.pause(0.00001)

			else:
				print ("Done")
				print (current_solution)
				break

			step += 1


		# Saving the results
		# df.to_csv(self.directory + "/GAValues.csv")

		# if should_plot:
		# 	print ("About to draw plot")
		# 	plt.clf()
		# 	plt.ioff()
		# 	x = [i for i in range (len(best_values))]
		# 	for col in df.columns:
		# 		plt.plot(x, df[col])
		# 	plt.savefig(self.directory + "/GAValues.png")
	





