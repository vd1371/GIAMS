#Loading dependencies
from .BaseUserCost import BaseUserCost
from utils.PredictiveModels.Linear import Linear

class DummyUserCost(BaseUserCost):
	def __init__(self, **params):
		super().__init__(**params)
		self.linear_model = Linear(X0 = 1, drift = 0, settings = self.settings)

	def predict_series(self, project_duration, random = True):
		'''Method for predicting the user costs in time'''
		return 3 * self.linear_model.predict_series(random)
		# The out put will be 1000 dollars