from .BaseDeterioration import BaseDeterioration
import numpy as np

class ContinuousYang2020(BaseDeterioration):

	def __init__(self, initial_condition = 1,
						lambda_ = 0.02,
						exponent = 1)

		"""
		Yang, D. Y., and Frangopol, D. M. (2020). “Life-cycle management of deteriorating bridge
		networks with network-level risk bounds and system
		reliability analysis.” Structural Safety, Elsevier, 83, 101911.
		the general form is condiiton = condition_initial - deterioration_rate * age ** exponent
		"""
		self.initial_condition = initial_condition
		self.lambda_ = lambda_
		self.exponent = exponent

	def predict_condition(self, previous_condition = 0, age = None):

		condition = self.initial_condition - self.lambda_ * age ** self.exponent

		return condition