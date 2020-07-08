import numpy as np

class BaseUtility(object):

	def __init__(self):
		super().__init__()

	def get(self, previous_condition, new_condition):
		raise self.utility_function(previous_condition) - self.utility_function(new_condition)
	