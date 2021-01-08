#Loading dependencies
from utils.GeneralSettings import *

class BaseRecovery:
	def __init__(self, **params):
		'''Parent object for all future recovery models
		
		::params::
		settings
		'''
		self.settings = params.pop('settings')

	def recovery_effectiveness(self, previous_state, action):
		raise NotImplementedError ("mrr_effectiveness is not implemented yet")