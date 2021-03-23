import numpy as np

from .BaseDeterioration import BaseDeterioration

class Markovian(BaseDeterioration):

	def __init__(self, probs_list):
		super().__init__()
		"""
		The probs_list must contains the transition probabilities of each state ti itself
		A system of 5 states must have the probs_list of length equal to 5
		"""
		self.probs_list = probs_list

	def predict_condition(self, previous_condition = 0, t = None, **kwargs):
		'''To predict the condition rating after one time step given some information'''
		if np.random.rand() > self.probs_list[previous_condition]:
			return previous_condition + 1
		else:
			return previous_condition