import numpy as np
from scipy.stats import norm
from copy import deepcopy

from .BaseResponse import BaseResponse

MEDIAN = 0 # It's just an index, to make it more clear to read
BETA = 1 # It's just an index, to make it more clear to read

class DummyResponse(BaseResponse):

	def __init__(self, asset):
		super().__init__(asset)
		'''Dummy response for buildings'''
		self.mapped_conditions = [0, 1, 2, 3, 4]

	def get(self):
		'''Finding the corresponding damage state'''
		idx = np.random.choice([0, 1, 2, 3, 4], p = [0.9, 0.05, 0.3, 0.2, 0])
		ds = ['ds1', 'ds2', 'ds3', 'ds4', 'ds5'][idx]
		mapped_condition = self.mapped_condition[idx]
			
		if mapped_condition > previous_condition:
			return mapped_condition, ds
		else:
			return previous_condition, 'ds1'

