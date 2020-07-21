from utils.GeneralSettings import *

class BaseMRREffectivenessModel(GenSet):
	
	def __init__(self):
		super().__init__()

	def get(self, previous_state, action):
		raise NotImplementedError ("mrr_effectiveness is not implemented yet")