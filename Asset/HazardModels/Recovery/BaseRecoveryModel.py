from utils.GeneralSettings import GenSet

class BaseRecoveryModel(GenSet):
	
	def __init__(self):
		super().__init__()

	def recovery_effectiveness(self, previous_state, action):
		raise NotImplementedError ("mrr_effectiveness is not implemented yet")