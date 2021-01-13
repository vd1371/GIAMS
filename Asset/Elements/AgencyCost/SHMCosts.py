from .BaseAgencyCost import BaseAgencyCost
from utils.PredictiveModels.Linear import Linear
from utils.GeneralSettings import *

class RetrofitCosts(BaseAgencyCost):

	def __init__(self):
		self.linear_model = Linear(X0 = 1, drift = 0, settings = self.settings)
		pass

	def first_inspection_cost(self, random):
		return 1 * self.linear_model.predict_series(random) / 1000

	def further_inspection_cost(self, random):
		return 10 * self.linear_model.predict_series(random) / 1000

	def action_costs(self, random):
		return 100 * self.linear_model.predict_series(random) / 1000

	def predict_series(self, random):
		return {INSP1: self.first_inspection_costs(random),
				INSP2: self.further_inspection_costs(random),
				DOMNT: self.action_costs(random)}

