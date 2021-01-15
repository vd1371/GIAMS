#Loading dependencies
import time
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
from pyswarms.discrete import BinaryPSO
from ._objectives import LCASolution
from ._objectives import _eval_sol

class PSO:

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
		self.dimensions = n_assets * asset_mrr_shape[0] * asset_mrr_shape[1]

	def _solut_to_1d_shape(self, solut):
		return solut.reshape(-1)

	def _solut_to_original_shape(self, solut):
		return np.array(solut).reshape(self.solut_shape)

	def set_hyperparameters(self, **params):

		c1 = params.pop('c1', 0.5)
		c2 = params.pop('c2', 0.5)
		w = params.pop('w', 0.9)
		k = params.pop('k', 30)
		p = params.pop('p', 2)

		self.pso_options = {'c1': c1, 'c2': c2, 'w': w, 'k': k, 'p': p}
		self.n_particles = params.pop('n_particles', 100)
		self.n_jobs = params.pop('n_jobs', 1)
		self.iter = params.pop('iter', 100)

		self.log.info((f"PSO optimization is started. \n"
					f"Options: {self.pso_options} \n"
					f"n_particles: {self.n_particles} \n"
					f"n_jobs: {self.n_jobs} \n"
					f"iter: {self.iter}"
					))

	def _pso_obj(self, x):

		# Creting the solutions objects
		solution_holder = []
		for particle in x:

			new_solut = self._solut_to_original_shape(particle)
			new_solut = LCASolution(lca = self.lca,
								solut = new_solut,
								obj_func = self.lca_ref.network.objective)
			solution_holder.append(new_solut)

		# Evaluating the Solutions
		results = []
		if self.n_jobs == 1:
			for i, sol in enumerate(solution_holder):
				start = time.time()
				results.append(_eval_sol_val(sol))

		else:
			with mp.Pool(max(-self.n_jobs * mp.cpu_count(), self.n_jobs)) as P:
				results = P.map(_eval_sol_val, solution_holder)

		return np.array(results)

	def optimize(self, verbose = 2):

		optimizer = BinaryPSO(n_particles = self.n_particles,
								dimensions = self.dimensions,
								options = self.pso_options)

		cost , pos = optimizer.optimize(self._pso_obj,
										iters = self.iter,
										verbose = verbose)

		print (cost)
		print (pos)
			




def _eval_sol_val(sol):
	sol.evaluate()
	return -sol.value

