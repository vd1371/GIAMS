from .BaseRecovery import BaseRecovery

class DummyRecovery(BaseRecovery):
	
	def __init__(self):
		super().__init__()

	def get(self, after_hazard_condition):

		actions = {1: self.DONOT, 2: self.DONOT, 3: self.DONOT, 4: self.BINAR}
			
		return 1, actions[after_hazard_condition]
