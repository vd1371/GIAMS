import numpy as np
from .BaseUtility import BaseUtility

class DummyUtility(BaseUtility):

	def __init__(self):
		super().__init__()

	def utility_function(self, x):
		return 100 * (1 - np.exp(-0.19 * x))
	