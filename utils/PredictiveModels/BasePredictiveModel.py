
from utils.GeneralSettings import GenSet

class BasePredictiveModel(GenSet):
	
	def __init__(self, X0):
		super().__init__()
		'''
		This is the base model for all of the predictor mdoels such as cost predictors, raffic models, etc.
		'''
		self.X0 = X0

	def set_model(**kwargs):
		raise NotImplementedError ("The set_model method of the module is not implemented yet")

	def predict(self):
		raise NotImplementedError ("The predict method of the module is not implemented yet")

	def predict_series(self):
		raise NotImplementedError ("The predict_series method of the module is not implemented yet")