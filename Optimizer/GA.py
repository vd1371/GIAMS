#Loading dependencies
import time
import numpy as np
import pandas as pd
from deap import tools
import matplotlib.pyplot as plt

import multiprocessing as mp
import ast
from ._objectives import LCASolution
from ._objectives import _eval_sol

class GA:
	def __init__(self, lca = None):
		'''Genetic algorithm for project-level optimization
	
		Therefore, it is expected that only one asset is analyzed
		'''

		# Objective_function is an instance of lca
		self.lca = lca

		# Gettign one instance the objective function
		self.lca_ref = lca()

		# lca has network, directory, log, and 
		self.directory = self.lca_ref.directory
		self.log = self.lca_ref.log

		asset_mrr_shape = self.lca_ref.network.assets[0].mrr_model.mrr.shape
		self.n_assets = len(self.lca_ref.network.assets)
		assert self.n_assets == 1, 'Only 1 asset must be used for GA'

		# It will be used to reshape the solution to 1d and original shape
		self.solut_shape = (self.n_assets, asset_mrr_shape[0], asset_mrr_shape[1])
		self.dimension = self.n_assets * asset_mrr_shape[0] * asset_mrr_shape[1]

		# To prevent double checking the checked Solutions
		self.taboo_list = []

	def _add_to_taboo_list(self, solut):
		self.taboo_list.append(hash(solut.tostring()))

	def _is_in_taboo_list(self, solut):
		return hash(solut.tostring()) in self.taboo_list

	def _solut_to_1d_shape(self, solut):
		return solut.reshape(-1)

	def _solut_to_original_shape(self, solut):
		return np.array(solut).reshape(self.solut_shape)

	def _solut_to_validation_shape(self, solut):
		return np.array(solut).reshape(self.validation_shape)

	def set_hyperparameters(self, **params):

		self.crossver_prob = params.pop('crossver_prob', 0.75)
		self.mutation_prob = params.pop('mutation_prob', 0.02)
		self.population_size = params.pop('population_size', 10)
		self.n_generations = params.pop('n_generations', 200)
		self.n_elites = params.pop('n_elites', 5)
		self.n_jobs = params.pop('n_jobs', 1)
		
		self.validation_dimension = params.pop('validation_dimension', 3)
		self.validation_shape = (self.n_assets,
								self.validation_dimension,
								int(self.dimension/self.validation_dimension))
		
		self.solution_class = LCASolution
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
					f"Validation dimension: {self.validation_dimension} \n"
					f"Validation shape: {self.validation_shape}"
					))

		'''
		This array of probability will be used in the selection phase. The selection method is Ranking selection
		The worst: 1, second worst:2, .... Then they all will be devided by the sum so sum of probabilities be 1
		'''
		pop_size = self.population_size
		self.p = [(pop_size - i) / ((pop_size + 1)*pop_size/2) for i in range(pop_size)]


	def init_gener(self):
		'''
		The proportion of 1 in the initial solut would be [0.1, 0.2, 0.3, 0.4, 0.5]
		Higher probabilities would lead to higher costs, therefore, 0.5 would be the biggest proportion

		This specific initiation is inspirer from Xuan, P., Guo, M.Z., Wang, J., Wang, C.Y., Liu, X.Y. and Liu, Y., 2011.
		Genetic algorithm-based efficient feature selection for classification of pre-miRNAs. Genetics and molecular research, 10(2), pp.588-603.
		'''
		gener = []
		start = time.time()
		while len(gener) < self.population_size:

			if not self.should_validate:
				for p in [0.1, 0.2, 0.3, 0.4, 0.5]:
					solut = np.random.choice([0,1], size = self.solut_shape, p = [1-p, p])
					new_sol = self.solution_class(lca = self.lca,
										solut = solut,
										obj_func = self.lca_ref.network.objective)
					if new_sol.is_valid():
						gener.append(new_sol)
					self._add_to_taboo_list(solut)

			else:
				solut = self.solution_class(shape = self.validation_shape)
				solut.random_init()
				gener.append(solut)

			thresh = 10
			if (time.time()-start > thresh):
				start = time.time()
				print (f"{thresh} seconds has passed but not enough offsprings could be generated given the conditions")
				print (f"{len(gener)} offsprings have been created so far")

		print ("First generation is initiated")

		return gener[:self.population_size]

	def mate(self, parent1, parent2):

		# Changing the shapes to 1d
		solut1, solut2 = self._solut_to_1d_shape(parent1.get_solut()), self._solut_to_1d_shape(parent2.get_solut())

		# Two point crossover
		if np.random.random() < self.crossver_prob:
			solut1, solut2 = tools.cxTwoPoint(solut1, solut2)

		# Flipbit mutation
		solut1 = tools.mutFlipBit(solut1, self.mutation_prob)
		solut2 = tools.mutFlipBit(solut2, self.mutation_prob)

		if not self.should_validate:
			solut1, solut2 = self._solut_to_original_shape(solut1), self._solut_to_original_shape(solut2)
		
		else:
			solut1, solut2 = self._solut_to_validation_shape(solut1), self._solut_to_validation_shape(solut2)
			
		return solut1, solut2

	def next_gener(self, gener):

		# Initating the next_gener holder
		next_gener = []

		# Ellitism
		for i in range(self.n_elites):
			if not self.should_validate:
				new_sol = LCASolution(lca = self.lca, 
									solut = gener[i].get_solut(),
									val = gener[i].value,
									flag = 'Elite',
									obj_func = self.lca_ref.network.objective)
			else:
				new_sol = self.solution_class(solut = gener[i].get_solut(),
											val = gener[i].value,
											flag = 'Elite',
											shape = self.validation_shape)
			next_gener.append(new_sol)

		start = time.time()
		while len(next_gener) < self.population_size:

			# Selecting parents
			parent1, parent2 = np.random.choice(gener, size = (2,), p= self.p, replace = False)

			# Creatings offsprings
			solut1, solut2 = self.mate(parent1, parent2)

			# Adding offsprings to the next generation
			for solut in [solut1, solut2]:

				if not self._is_in_taboo_list(solut):

					if not self.should_validate:
						offspring = LCASolution(lca = self.lca,
												solut = np.copy(solut),
												obj_func = self.lca_ref.network.objective)
					else:
						offspring = self.solution_class(solut = np.copy(solut),
													shape = self.validation_shape)
					
					if offspring.is_valid():
						next_gener.append(offspring)
						self._add_to_taboo_list(solut)

			if (time.time()-start > 60):
				start = time.time()
				print("60 seconds has passed but no offspring could be generated given the conditions, something could be wrong")

		# print ("creating the next_gener\n", next_gener)

		return next_gener[:self.population_size]

	def eval_gener(self, gener, n_gener):
		# Evaluating the objective function of the problem except the elites
		idx = self.n_elites if n_gener != 0 else 0
		elites, to_be_eval = gener[:idx], gener[idx:]

		# Evaluating the Solutions
		# We don't need parallel processing for validation function
		if self.n_jobs == 1 or self.should_validate:
			for i, sol in enumerate(to_be_eval):
				start = time.time()
				sol.evaluate()
				print (f"sol {i} in {time.time()-start:.2f}")

		# Parallel processing
		else:
			with mp.Pool(max(-self.n_jobs * mp.cpu_count(), self.n_jobs)) as P:
				to_be_eval = P.map(_eval_sol, to_be_eval)
			
		# To prevent double calculating the elites values
		gener = to_be_eval if idx == 0 else elites + to_be_eval

		# Sorting the generation based on their value and the optimization type
		gener = sorted(gener, key=lambda x: x.value, reverse = self.sorting_order)

		return gener


	def optimize(self,
				should_plot = True,
				should_plot_live = False,
				rounds = 1,
				label = 'GA',
				should_validate = False):

		self.should_validate = should_validate

		# Creating a dataframe holder for the analysis
		self.taboo_list = []
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

				best_values.append(gener[0].value)

				# Plotting the value online
				if should_plot_live:
					plt.ion()
					plt.clf()
					plt.title(f'Gener {n_gener}')
					plt.xlabel('Generation')
					plt.ylabel('Utility')
					
					plt.plot([i for i in range(len(best_values))], best_values, label="Best Solution")
					
					plt.legend()
					plt.grid(True, which = 'both')
					plt.draw()
					plt.pause(0.00001)

				n_gener += 1

			df[f'Values-Round{i}'] = best_values

		# Saving the results
		df.to_csv(self.directory + f"/{label}Values.csv")

		if should_plot:
			print ("About to draw plot")
			plt.clf()
			plt.ioff()
			x = [i for i in range (len(best_values))]
			for col in df.columns:
				plt.plot(x, df[col])
			plt.xlabel('Generation')
			plt.ylabel(f'{label} value')
			plt.savefig(self.directory + f"/{label}Values.png")


	def validate(self):

		from ._objectives import AxisParallel
		from ._objectives import DeJong
		from ._objectives import RotatedHyperEllipsoid
		from ._objectives import RosenbrockValley
		from ._objectives import Rastrigin
		from ._objectives import Schwefel
		from ._objectives import Griewangk

		test_dic = {'DeJong' : DeJong,
					'AxisParallel': AxisParallel,
					'RotatedHyperEllipsoid': RotatedHyperEllipsoid,
					'RosenbrockValley': RosenbrockValley,
					'Rastrigin': Rastrigin,
					'Schwefel' : Schwefel,
					'Griewangk': Griewangk}

		# test_dic = {'Griewangk': Griewangk}
		for k, v in test_dic.items():

			self.solution_class = v
			self.optimize(label = k,
							should_validate = True)

