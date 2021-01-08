#Loading dependencies
from utils.GeneralSettings import *

class BaseMRREffectiveness:
	def __init__(self, **params):
		'''Parent object for all future MRREffectiveness models
		
		::params::
		settings
		'''
		self.settings = params.pop('settings')

	def get(self, previous_state, action):
		raise NotImplementedError ("mrr_effectiveness is not implemented yet")