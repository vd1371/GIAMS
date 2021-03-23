#Loading dependencies
from utils.GeneralSettings import *

class BaseMRREffectiveness:
	def __init__(self, **params):
		'''Parent object for all future MRREffectiveness models
		
		::params::
		settings
		'''
		self.settings = params.pop('settings')

	def get(self, **kwargs):
		'''To make sure all future effectiveness models have get method'''
		raise NotImplementedError ("mrr_effectiveness is not implemented yet")