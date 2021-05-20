#Loading dependencies
from .BaseRecovery import *

class SimpleRecovery(BaseRecovery):
	
	def __init__(self, **params):
		super().__init__(**params)
		'''A simple recovery scenario'''
		self.actions = {1: DONOT, 2: DONOT, 3: MAINT, 4: MAINT, 5: REHAB, 6: RECON, 7: RECON}
		self.possible_actions = list(self.actions.keys())

	def get(self, after_hazard_condition):
		'''Getting the policy based on the after hazard state'''
		if not after_hazard_condition in self.possible_actions:
			raise ValueError ('After hazard condition is not in the possible actions')
			
		if not self.actions[after_hazard_condition] == RECON:
			return 1, self.actions[after_hazard_condition]
		else:
			return 0, self.actions[RECON]