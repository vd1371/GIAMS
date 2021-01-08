class BaseUserCost:
	def __init__(self, **params):
		'''Parent object for all future recovery models
		
		::params::
		settings
		'''
		self.settings = params.pop('settings')

	def set_asset(self, asset):
		self.asset = asset

	def predict_series(self):
		raise NotImplementedError ("predict_series of user cost model is not implemented yet")
