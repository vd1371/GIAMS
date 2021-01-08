#Loading dependencies
import numpy as np
from .GeneralSettings import *
from .NPV import NPV

class Container:
	def __init__(self, **params):
		'''This is a holder for results
		
		All simulation results shall be kept in this contatiner
		'''
		self.settings = params.pop('settings')
		self.npv_samples = []
		self.stepwise = np.zeros(self.settings.n_steps)
		self.simulator_counter = 0

	def update_stepwise(self, stepwise_vals):

		self.stepwise = (self.stepwise * self.simulator_counter + stepwise_vals) / \
								(self.simulator_counter + 1)
		self.simulator_counter += 1

	def add_to_npv_samples(self, val):
		self.npv_samples.append(val)

	def at_year(self, year = 0):
		idx = int(year/self.settings.dt)
		return self.stepwise[idx]

	def expected(self):
		return round(np.average(np.array(self.npv_samples)),2), \
						round(np.std(np.array(self.npv_samples)),2)

	def get_samples(self):
		return self.npv_samples

	def get_stepwise(self):
		return self.stepwise

