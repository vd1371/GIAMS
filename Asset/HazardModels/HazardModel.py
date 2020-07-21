'''
This class is basically the holder of all hazard sub-models
'''

class HazardModel:

	def __init__(self):
		pass

	def set_asset(self, asset):
		self.asset = asset

	def set_generator_model(self, model):
		self.generator = model

	def set_response_model(self, model):
		self.response = model

	def set_loss_model(self, model):
		model.set_asset(self.asset)
		self.loss = model

	def set_recovery_model(self, model):
		self.recovery = model