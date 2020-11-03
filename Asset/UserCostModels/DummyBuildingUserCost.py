from .BaseUserCost import BaseUserCost

from utils.PredictiveModels.Linear import Linear

class DummyUserCost(BaseUserCost):

	def __init__(self):
		super().__init__()

		self.linear_model = Linear(1, 0)

	def predict_series(self, project_duration, random = True):

		return 3 * self.linear_model.predict_series(random)
		# The out put will be 1000 dollars