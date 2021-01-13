#Loading dependencies
import numpy as np
from collections import Counter
from .BaseMRRPlan import *

class SHMActions(BaseMRRPlan):
	def __init__(self, **params):
		super().__init__(**params)
		'''Dummy module for SHM analysis
		
		This module is developed per request of reviewers who
		required implementation of SHM in GIAMS.	
		'''
		self.randomize_mrr()

	def set_mrr(self, new_mrr):
		if np.shape(new_mrr) != (self.settings.n_elements, self.settings.n_steps*self.settings.dt):
			raise ValueError(f"Expected shape of mrr is {(self.settings.n_elements, self.settings.n_steps*self.settings.dt)}"\
								f"But {new_mrr.shape} was given")
		self.mrr = new_mrr

	def randomize_mrr(self):
		self.mrr = np.random.randint(2, size=(self.settings.n_elements, self.settings.dt*self.settings.n_steps))
		return self.mrr

	def mrr_to_decimal(self, mrr_binary = None):

		if mrr_binary is None:
			mrr = self.mrr
		else:
			mrr = mrr_binary

		self.mrr_decoded = []
		for element_idx in range (self.settings.n_elements):
			element_mrr = []
			for j in range(0, len(mrr[element_idx]), 2):
				element_mrr.append(int(str(int(mrr[element_idx][j]*10+ mrr[element_idx][j+1])), 2))
			self.mrr_decoded.append(element_mrr)

		return self.mrr_decoded

	def mrr_to_binary(self, decoded_mrr):
		
		self.mrr = []
		for i in range(len(decoded_mrr)):
			temp_mrr = []
			for val in decoded_mrr[i]:
				for binar in bin(val)[2:]:
					temp_mrr.append(binar)
			self.mrr.append(temp_mrr)

		return self.mrr

	def check_policy(self):
		'''Dummy check_policy method'''
		return True