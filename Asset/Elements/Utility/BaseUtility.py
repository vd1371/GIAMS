import numpy as np
class BaseUtility(object):

	def __init__(self):
		super().__init__()
		'''Parent class of all future utility function'''

	def get(self, previous_condition, new_condition):

		if isinstance(previous_condition, (list,np.ndarray)):
			util_result = self.utility_function(previous_condition) - self.utility_function(new_condition)
			util_result[util_result<0] = 0

		elif isinstance(previous_condition, (float, int, np.integer, np.floating)):
			util_result = max(self.utility_function(previous_condition) - self.utility_function(new_condition), 0)
			
		else:
			raise ValueError (f"Something is wrong at the BaseUtility with the conditions: perhaps {previous_condition}")

		return util_result