from .BaseAgencyCost import BaseAgencyCost
from utils.PredictiveModels.Linear import Linear
from utils.GeneralSettings import *

class RetrofitCosts(BaseAgencyCost):

	def __init__(self):
		self.linear_model = Linear(1, 0)
		pass

	def retrofit_costs(self, random):
		return 100 * self.linear_model.predict_series(random) / 1000

	def predict_series(self, random):
		return {self.BINAR: self.retrofit_costs(random)}

