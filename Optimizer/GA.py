import time
import numpy as np
from deap import tools
import matplotlib.pyplot as plt

import multiprocessing as mp


class Individual:

	def __init__(self, lca, chrom = None, val = None, flag = 'Regular'):
		
		self.lca = lca
		self.chrom = chrom
		self.value = val
		self.flag = flag

	def evaluate(self):

		self.lca_model = self.lca()
		self.lca_model.network.set_network_mrr(self.get_chrom())
		self.lca_model.run()

		if self.is_in_budget():
			self.value = self.lca_model.get_network_npv()[2]
		else:
			self.value = -1000

	def is_valid(self):

		lca = self.lca()
		for asset in lca.network.assets:

			if not asset.mrr_model.check_policy():
				# To check whether the mrr meets certain policies
				# For example only two reconstrcution for an element in the horizon
				return False
		return True

	def is_in_budget(self):

		def exceed_yearly_budget_against_costs(budgets, costs):

			for budget, cost in zip(budgets, costs):
				if cost > budget:
					return True
			return False

		if self.lca_model.get_year_0()[1] > self.lca_model.network.current_budget_limit:
			# To check whether the plan meets the current budget
			return False

		elif self.lca_model.get_network_npv()[1] > self.lca_model.network.npv_budget_limit:
			# To put a cap on the npv of the MRR plan
			return False

		elif exceed_yearly_budget_against_costs(self.lca_model.network.budget_model.predict_series(random = False), self.lca_model.get_network_stepwise()[1]):
			# To check whether the predicted costs and budget suits each other
			return False

		return True

	def set_value(self, val):
		self.value = val

	def set_chrom(self, chrom):
		self.chrom = chrom

	def get_chrom(self):
		return np.copy(self.chrom)

	def __repr__(self):
		return f"Ind {self.flag} - {hash(self.chrom.tostring())} - {self.chrom} - Val:{self.value}"
	
	def __str__(self):
		return f"Ind {self.flag} - {hash(self.chrom.tostring())} - {self.chrom} - Val:{self.value}"

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

		# Initializing the GA characteristics
		self.set_ga_chars()

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

	def set_ga_chars(self, crossver_prob = 0.75,
							mutation_prob = 0.02,
							population_size = 10,
							n_generations = 200,
							n_elites = 5,
							optimzition_type = 'min',
							n_jobs = 1):
		self.crossver_prob = crossver_prob
		self.mutation_prob = mutation_prob
		self.population_size = population_size
		self.n_generations = n_generations
		self.n_elites = n_elites
		self.n_jobs = n_jobs

		if optimzition_type == 'min':
			self.sorting_order = False
		elif optimzition_type == 'max':
			self.sorting_order = True
		else:
			raise ValueError ("Wrong value for the optimzition_type, it should either max or min")

		self.log.info((f"Genetic algorithm optimization is started. \n"
					f"Crossover Probability: {crossver_prob} \n"
					f"Mutation Probability: {mutation_prob} \n"
					f"Population Size: {population_size} \n"
					f"Number of generations: {n_generations} \n"
					f"Number of elites: {n_elites} \n"
					f"Optimization type: {optimzition_type} \n"
					))

		'''
		This array of probability will be used in the selection phase. The selection method is Ranking selection
		The worst: 1, second worst:2, .... Then they all will be devided by the sum so sum of probabilities be 1
		'''
		self.p = [(population_size - i) / ((population_size + 1)*population_size/2) for i in range(population_size)]


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
				new_ind = Individual(self.lca, chrom = chrom)
				if new_ind.is_valid():
					gener.append(new_ind)
				self._add_to_taboo_list(chrom)
			
			if len(gener) == self.population_size:
				break

			if (time.time()-start > 60):
				start = time.time()
				print("60 seconds has passed but no offspring could be generated given the conditions, something could be wrong")

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
		
		# Sorting the generation based on their value and the optimization type
		gener = sorted(gener, key=lambda x: x.value, reverse = self.sorting_order)

		# Ellitism
		for i in range(self.n_elites):
			new_ind = Individual(self.lca, gener[i].get_chrom(), gener[i].value, 'Elite')
			next_gener.append(new_ind)

		start = time.time()
		while len(next_gener) < self.population_size:

			# Selecting parents
			parent1, parent2 = np.random.choice(gener, size = (2,), p= self.p, replace = False)

			# Creatings offsprings
			chrom1, chrom2 = self.mate(parent1, parent2)

			# Adding offsprings to the next generation
			if not self._is_in_taboo_list(chrom1):

				offspring1 = Individual(self.lca, chrom1)
				if offspring1.is_valid():
					next_gener.append(offspring1)

			if not self._is_in_taboo_list(chrom2):
				
				offspring2 = Individual(self.lca, chrom2)
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

		# Evaluating the individuals
		with mp.Pool(max(-self.n_jobs * mp.cpu_count(), self.n_jobs)) as P:
			eval_gener = P.map(_eval_ind, gener[idx:])
		eval_gener = gener[:idx] + eval_gener

		# for ind in gener:
		# 	ind.evaluate()

		return eval_gener


	def optimize(self, should_plot = True):

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
			for i in range (self.population_size):
				log_str += f"Gener: {n_gener} - {gener[i]} - TabooListLength: {len(self.taboo_list)} \n"
			best_values.append(max(gener[0].value, 0))

			self.log.info(log_str)
			print (f"Gener: {n_gener} - {gener[0]} - TabooListLength: {len(self.taboo_list)} - Timme elapsed: {time.time()-start:.2f}")

			# Plotting the value online
			if should_plot:
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

		df = pd.DataFrame()
		df['index'] = [i for i in range(len(best_values))]
		df['value'] = best_values
		df.to_csv(self.directory + "/GAValues.csv")

		if should_plot:
			plt.savefig(self.directory + "/GAValues.png")
	





