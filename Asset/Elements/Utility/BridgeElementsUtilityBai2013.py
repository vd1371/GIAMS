import numpy as np
from .BaseUtility import BaseUtility

"""
TheReference
Q. Bai, S. Labi, K.C. Sinha, P.D. Thompson, Multiobjective optimization for
project selection in network-level bridge management incorporating
decision-maker’s preference using the concept of holism, J. Bridg. Eng. 18 
(2013) 879–889. doi:10.1061/(ASCE)BE.1943-5592.0000428.
"""

class DeckUtility(BaseUtility):

	def __init__(self):
		super().__init__()

	def utility_function(self, x):
		return 122.75 * (1 - np.exp(-0.19 * x))

class SuperstructureUtility(BaseUtility):

	def __init__(self):
		super().__init__()

	def utility_function(self, x):
		return 119.13 * (1 - np.exp(-0.203 * x))

class SubstructureUtility(BaseUtility):

	def __init(self):
		super().__init__()

	def utility_function(self, x):
		return 119.49 * (1 - np.exp(-0.203 * x))

class WearingUtiliy(BaseUtility):

	def __init(self):
		super().__init__()

	def utility_function(self, x):
		return 100 / (1 + np.exp(-1.38 * x + 7.925))
	