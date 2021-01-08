#Loading dependencies
from .BaseRecovery import *

class SimpleRecovery(BaseRecovery):
	
	def __init__(self, **params):
		super().__init__(**params)

	def get(self, after_hazard_condition):

		actions = {1: DONOT, 2: DONOT, 3: MAINT, 4: MAINT, 5: REHAB, 6: RECON, 7: RECON}

		if not actions[after_hazard_condition] == RECON:
			return 1, actions[after_hazard_condition]
		else:
			return 0, actions[RECON]