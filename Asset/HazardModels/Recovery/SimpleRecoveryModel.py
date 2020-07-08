from .BaseRecoveryModel import BaseRecoveryModel

class SimpleRecoveryModel(BaseRecoveryModel):
	
	def __init__(self):
		super().__init__()

	def get_effectiveness(self, next_condition):

		actions = {2: self.MAINT, 3: self.REHAB, 4: self.RECON, 5: self.RECON}
		return 0, actions[next_condition]