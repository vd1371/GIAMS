class BasePredictiveModel:
	
	def __init__(self, **params):
		'''Parent object for all predictive models

		This is the base model for all of the predictor
		mdoels such as cost predictors, raffic models, etc.
		'''
		self.X0 = params.pop('X0')
		self.settings = params.pop('settings')

	def set_model(**kwargs):
		raise NotImplementedError ("The set_model method of the module is not implemented yet")

	def predict(self):
		raise NotImplementedError ("The predict method of the module is not implemented yet")

	def predict_series(self):
		raise NotImplementedError ("The predict_series method of the module is not implemented yet")