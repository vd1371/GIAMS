import numpy as np
from .BaseHazard import *

class PoissonProcess(BaseHazard):

	def __init__(self, occurrence_rate = 0.018, dist = None):
		super().__init__()
		'''PoissonProcess class for generating hazards'''
		self.set_occurrence_rate(occurrence_rate)
		self.set_magnitude_distribution(dist)

	def set_occurrence_rate(self, val):
		'''Set the occurrence rate of the poisson process'''
		assert isinstance(val, float), 'float should be passed'
		self.occurrence_rate = val

	def set_magnitude_distribution(self, dist):
		'''Set the magnitude distribution of the poisson process'''
		if not 'Distributions' in str(type(dist)):
			raise ValueError ("passed dist must be a distribution type")
		self.dist = dist

	def generate_one_instance(self):
		'''
		meanfloat or array_like of floats, optional
		Mean value of the underlying normal distribution. Default is 0.
		sigmafloat or array_like of floats, optional
		Standard deviation of the underlying normal distribution. Must be non-negative. Default is 1.
		'''
		return self.dist.sample()

	def generate_one_lifecycle(self, start = 0, horizon = 20, dt = 2):
		'''Generating the hazards in a life cyle
		returns a disctioner with years as keys and magnitude of hazards as values
		'''
		hazard = {}

		time = start
		while time < horizon:
			time += -1*np.log(1-np.random.random())/self.occurrence_rate
			if not time > horizon:
				hazard[int(time//dt)*dt] = self.dist.sample()

		return hazard