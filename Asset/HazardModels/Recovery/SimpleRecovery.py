from .BaseRecovery import BaseRecovery

class SimpleRecovery(BaseRecovery):
	
	def __init__(self):
		super().__init__()

	def get(self, after_hazard_condition):

		actions = {1: self.DONOT, 2: self.DONOT, 3: self.MAINT, 4: self.MAINT, 5: self.REHAB, 6: self.RECON, 7: self.RECON}

		if not actions[after_hazard_condition] == self.RECON:
			return 1, actions[after_hazard_condition]
		else:
			return 0, actions[self.RECON]