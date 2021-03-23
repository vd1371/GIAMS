#Loading dependencies
import numpy as np

class BaseDistribution(object):
	def __init__ (self):
		super().__init__()
		#Adding the generator
		self.generator = np.random.default_rng()

	def set(self):
		raise NotImplementedError ("set is not implemented yet")

	def sample(self):
		raise NotImplementedError ("sample is not implemented yet")
