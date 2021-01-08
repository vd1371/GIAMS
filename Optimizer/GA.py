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

class GA:
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

	def set_obj_func(self, obj_func):
		self.obj_func = obj_func

	def set_ga_chars(self, **params):

		self.crossver_prob = params.pop('crossver_prob', 0.75)
		self.mutation_prob = params.pop('mutation_prob', 0.02)
		self.population_size = params.pop('population_size', 10)
		self.n_generations = params.pop('n_generations', 200)
		self.n_elites = params.pop('n_elites', 5)
		self.n_jobs = params.pop('n_jobs', 1)
		optimization_type = params.pop('optimization_type', 'max')

		if optimization_type == 'min':
			self.sorting_order = False
		elif optimization_type == 'max':
			self.sorting_order = True
		else:
			raise ValueError ("Wrong value for the optimzition_type, it should either max or min")

		self.log.info((f"Genetic algorithm optimization is started. \n"
					f"Crossover Probability: {self.crossver_prob} \n"
					f"Mutation Probability: {self.mutation_prob} \n"
					f"Population Size: {self.population_size} \n"
					f"Number of generations: {self.n_generations} \n"
					f"Number of elites: {self.n_elites} \n"
					f"Optimization type: {optimization_type} \n"
					))

		'''
		This array of probability will be used in the selection phase. The selection method is Ranking selection
		The worst: 1, second worst:2, .... Then they all will be devided by the sum so sum of probabilities be 1
		'''
		pop_size = self.population_size
		self.p = [(pop_size - i) / ((pop_size + 1)*pop_size/2) for i in range(pop_size)]


	def init_gener(self):
		'''
		The proportion of 1 in the initial chrom would be [0.1, 0.2, 0.3, 0.4, 0.5]
		Higher probabilities would lead to higher costs, therefore, 0.5 would be the biggest proportion

		This specific initiation is inspirer from Xuan, P., Guo, M.Z., Wang, J., Wang, C.Y., Liu, X.Y. and Liu, Y., 2011.
		Genetic algorithm-based efficient feature selection for classification of pre-miRNAs. Genetics and molecular research, 10(2), pp.588-603.
		'''
		gener = []
		start = time.time()
		while True:
			for p in [0.1, 0.2, 0.3, 0.4, 0.5]:
				chrom = np.random.choice([0,1], size = self.chrom_shape, p = [1-p, p])
				new_ind = Individual(self.lca, chrom = chrom, obj_func = self.obj_func)
				if new_ind.is_valid():
					gener.append(new_ind)
				self._add_to_taboo_list(chrom)
			
			if len(gener) >= self.population_size:
				break

			thresh = 10
			if (time.time()-start > thresh):
				start = time.time()
				print (f"{thresh} seconds has passed but not enough offsprings could be generated given the conditions")
				print (f"{len(gener)} offsprings have been created so far")

		print ("First generation is initiated")

		return gener[:self.population_size]

	def mate(self, parent1, parent2):

		# Changing the shapes to 1d
		chrom1, chrom2 = self._chrom_to_1d_shape(parent1.get_chrom()), self._chrom_to_1d_shape(parent2.get_chrom())

		# Two point crossover
		if np.random.random() < self.crossver_prob:
			chrom1, chrom2 = tools.cxTwoPoint(chrom1, chrom2)

		# Flipbit mutation
		chrom1 = tools.mutFlipBit(chrom1, self.mutation_prob)
		chrom2 = tools.mutFlipBit(chrom2, self.mutation_prob)

		chrom1, chrom2 = self._chrom_to_original_shape(chrom1), self._chrom_to_original_shape(chrom2)

		return chrom1, chrom2

	def next_gener(self, gener):

		# Initating the next_gener holder
		next_gener = []

		# Ellitism
		for i in range(self.n_elites):
			new_ind = Individual(self.lca, 
								chrom = gener[i].get_chrom(),
								val = gener[i].value,
								flag = 'Elite',
								obj_func = self.obj_func)
			next_gener.append(new_ind)

		start = time.time()
		while len(next_gener) < self.population_size:

			# Selecting parents
			parent1, parent2 = np.random.choice(gener, size = (2,), p= self.p, replace = False)

			# Creatings offsprings
			chrom1, chrom2 = self.mate(parent1, parent2)

			# Adding offsprings to the next generation
			if not self._is_in_taboo_list(chrom1):

				offspring1 = Individual(self.lca, np.copy(chrom1), obj_func = self.obj_func)
				if offspring1.is_valid():
					next_gener.append(offspring1)

			if not self._is_in_taboo_list(chrom2):
				
				offspring2 = Individual(self.lca, np.copy(chrom2), obj_func = self.obj_func)
				if offspring2.is_valid():
					next_gener.append(offspring2)

			self._add_to_taboo_list(chrom1)
			self._add_to_taboo_list(chrom2)

			if (time.time()-start > 60):
				start = time.time()
				print("60 seconds has passed but no offspring could be generated given the conditions, something could be wrong")

		# print ("creating the next_gener\n", next_gener)

		return next_gener[:self.population_size]

	def eval_gener(self, gener, n_gener):
		# Evaluating the objective function of the problem except the elites
		idx = self.n_elites if n_gener != 0 else 0
		elites, to_be_eval = gener[:idx], gener[idx:]

		# Evaluating the individuals
		if self.n_jobs == 1:
			for i, ind in enumerate(to_be_eval):
				start = time.time()
				ind.evaluate()
				print (f"Ind {i} in {time.time()-start:.2f}")

		else:
			with mp.Pool(max(-self.n_jobs * mp.cpu_count(), self.n_jobs)) as P:
				to_be_eval = P.map(_eval_ind, to_be_eval)
			

		# To prevent double calculating the elites values
		gener = to_be_eval if idx == 0 else elites + to_be_eval

		# Sorting the generation based on their value and the optimization type
		gener = sorted(gener, key=lambda x: x.value, reverse = self.sorting_order)

		return gener


	def optimize(self,
				should_plot = True,
				should_plot_live = False,
				rounds = 1):

		# Creating a dataframe holder for the analysis
		df = pd.DataFrame()

		for i in range(rounds):

			n_gener = 0
			best_values, gener_num_holder = [], []

			start = time.time()
			while n_gener < self.n_generations:
				# If certain criteria is met, break the loop
				### TODO: Write termination criteria

				if n_gener == 0:
					# CReating the first generation
					gener = self.init_gener()
				else:
					# Creating the new generation
					gener = self.next_gener(gener)

				# Evaluate the generation
				gener = self.eval_gener(gener, n_gener = n_gener)

				# Logging the results
				log_str = "\n"
				# for i in range (self.population_size):
				# 	log_str += f"Gener: {n_gener} - {gener[i]} - TabooListLength: {len(self.taboo_list)} \n"
				log_str += f"Round {i}  Gener: {n_gener} - {gener[0]} - "\
							f"TabooListLength: {len(self.taboo_list)} \n"
				print (f"Round {i}  Gener: {n_gener} - {gener[0]} - "\
							f"TabooListLength: {len(self.taboo_list)} - "\
							f"Timme elapsed: {time.time()-start:.2f}")
				self.log.info(log_str)

				best_values.append(max(gener[0].value, 0))

				# Plotting the value online
				if should_plot_live:
					plt.ion()
					plt.clf()
					plt.title(f'Gener {n_gener}')
					plt.xlabel('Generation')
					plt.ylabel('Utility')
					
					plt.plot([i for i in range(len(best_values))], best_values, label="Best individual")
					
					plt.legend()
					plt.grid(True, which = 'both')
					plt.draw()
					plt.pause(0.00001)

				n_gener += 1

			df[f'Values-Round{i}'] = best_values

		# Saving the results
		df.to_csv(self.directory + "/GAValues.csv")

		if should_plot:
			print ("About to draw plot")
			plt.clf()
			plt.ioff()
			x = [i for i in range (len(best_values))]
			for col in df.columns:
				plt.plot(x, df[col])
			plt.savefig(self.directory + "/GAValues.png")
	





