class HazardModel:

	def __init__(self):
		'''Hazard model holder
		This class is basically the holder of all hazard sub-models
		'''
		pass

	def set_asset(self, asset):
		if not "AssetTypes" in str(type(asset)):
			raise ValueError ("asset must be an asset type like building")
		self.asset = asset

	def set_generator_model(self, model):
		if not "Generator" in str(type(model)):
			raise ValueError ("model must be a generator type")
		self.generator = model

	def set_response_model(self, model):
		if not "Response" in str(type(model)):
			raise ValueError ("model must be a Response type")
		self.response = model

	def set_loss_model(self, model):
		if not "Loss" in str(type(model)):
			raise ValueError ("model must be a loss type")
		model.set_asset(self.asset)
		self.loss = model

	def set_recovery_model(self, model):
		if not "Recovery" in str(type(model)):
			raise ValueError ("model must be a recovery type")
		self.recovery = model