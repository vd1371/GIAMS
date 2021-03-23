#Loading dependencies
from .BaseRecovery import *

class DummyRecovery(BaseRecovery):
	
	def __init__(self, **params):
		super().__init__(**params)

	def get(self, after_hazard_condition):
		'''Getting the policy based on the after hazard state'''
		actions = {1: DONOT, 2: DONOT, 3: DONOT, 4: BINAR}
		return 1, actions[after_hazard_condition]
