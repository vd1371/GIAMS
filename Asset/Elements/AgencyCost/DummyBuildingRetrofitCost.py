from .BaseAgencyCost import BaseAgencyCost
from utils.PredictiveModels.Linear import Linear
from utils.GeneralSettings import *

def check_random(random):
	assert isinstance(random, bool), 'random must be boolean'

class RetrofitCosts(BaseAgencyCost):

	def __init__(self):
		self.linear_model = Linear(X0 = 1, drift = 0, settings = self.settings)
		pass

	def retrofit_costs(self, random):
		check_random(random)
		return 100 * self.linear_model.predict_series(random) / 1000

	def predict_series(self, random):
		return {BINAR: self.retrofit_costs(random)}

