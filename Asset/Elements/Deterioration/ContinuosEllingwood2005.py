from .BaseDeterioration import BaseDeterioration
import numpy as np

class ContinuousEllingwood2005(BaseDeterioration):

	def __init__(self, 	a = 0.02,
						b = 1)

		"""
		B.R. Ellingwood, Risk-informed condition assessment of civil infrastructure: 
		state of practice and research issues, Struct. Infrastruct. Eng. 1 (2005) 7–18.
		doi:10.1080/15732470412331289341
		the general form is condiiton = a * age ** b
		"""

		self.a = a
		self.b = b

	def predict_condition(self, previous_condition = 0, t = None):

		condition = self.initial_condition - self.lambda_ * t * self.exponent

		return condition