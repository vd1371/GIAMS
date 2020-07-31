import numpy as np
from .BaseHazard import *

class PoissonProcess(BaseHazard):

	def __init__(self, occurrence_rate = 0.018, dist = None):
		super().__init__()

		self.occurrence_rate = occurrence_rate
		self.dist = dist

	def set_occurrence_rate(self, val):
		self.occurrence_rate = val

	def set_magnitude_distribution(self, dist):
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
		hazard = {}

		time = start
		while time < horizon:
			time += -1*np.log(1-np.random.random())/self.occurrence_rate
			if not time > horizon:
				hazard[int(time//dt)*dt] = self.dist.sample()

		return hazard