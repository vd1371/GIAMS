# Loading dependencies
from .BasePredictiveModel import BasePredictiveModel
import numpy as np

class Exponential(BasePredictiveModel):

	def __init__(self, **params):
		super().__init__(**params)
		'''Exponentaial growth

		This is a exponential growth for future trends
		'''
		self.growth_rate = params.pop('growth_rate')
		self.x = self.predict_series(random = True)

	def predict(self, t = None):
		return self.X0 * np.exp(t*self.growth_rate)

	def predict_series(self, random = True):

		if random:
			T = np.linspace(0, self.settings.horizon, self.settings.n_steps)
			x = self.X0 * np.exp(T*self.growth_rate)
			return x
		else:
			return self.x