import numpy as np
from collections import Counter

from .BaseMRRPlan import *


class MRRTwoActions(BaseMRRPlan):
	
	def __init__(self, start = 0, action_duration = 0):
		super().__init__()

		self.start = 0
		self.mrr_duration = {self.BINAR: action_duration}
		
		self.randomize_mrr()

	def randomize_mrr(self):
		self.mrr = np.random.randint(2, size=(self.n_elements, self.n_steps))
		return self.mrr

	def mrr_to_decimal(self, mrr_binary = None):

		# In two actions, the decimal and binary are the same
		self.mrr_decoded = self.mrr if mrr_binary is None else mrr_binary
		return self.mrr_decoded

	def mrr_to_binary(self, decoded_mrr):
		# In two actions, the decimal and binary are the same
		self.mrr = decoded_mrr
		return self.mrr

	def check_policy(self):
		mrr_decimal = self.mrr_to_decimal()

		for elem_mrr in mrr_decimal:
			if np.sum(elem_mrr) > self.dt/2 :
				return False

		return True