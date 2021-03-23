#Loading dependencies
import numpy as np
from collections import Counter

from .BaseMRRPlan import *

class MRRTwoActions(BaseMRRPlan):
	
	def __init__(self, **params):
		super().__init__(**params)

		self.start = params.pop(start)
		
		action_duration = params.pop('action_duration')
		self.mrr_duration = {BINAR: action_duration}
		
		self.randomize_mrr()

	def randomize_mrr(self):
		'''Randomly initialize the mrr'''
		self.mrr = np.random.randint(2, size=(self.settings.n_elements, self.settings.n_steps))
		return self.mrr

	def mrr_to_decimal(self, mrr_binary = None):
		'''Converting the binray representation to decicaml representations'''
		self.mrr_decoded = self.mrr if mrr_binary is None else mrr_binary
		return self.mrr_decoded

	def mrr_to_binary(self, decoded_mrr):
		'''Converting the decimal representation to binray representations'''
		self.mrr = decoded_mrr
		return self.mrr

	def check_policy(self):
		'''Checking if a policy is acceptable'''
		mrr_decimal = self.mrr_to_decimal()

		for elem_mrr in mrr_decimal:
			if np.sum(elem_mrr) > self.settings.dt/2 :
				return False

		return True