from utils.GeneralSettings import GenSet

class BaseMRREffectivenessModel(GenSet):
	
	def __init__(self):
		super().__init__()

	def mrr_effectiveness(self, previous_state, action):
		raise NotImplementedError ("mrr_effectiveness is not implemented yet")