# Loading dependencies
from .BasePredictiveModel import BasePredictiveModel
import numpy as np

class Power(BasePredictiveModel):

	def __init__(self, **params):
		super().__init__(**params)
		'''Power growth model for predicting future trends

		::params::
		growth_rate
		'''
		self.growth_rate = params.pop('growth_rate')
		self.x = self.predict_series(random = True)

	def predict(self, T = None):
		return self.X0 * (1+self.growth_rate) ** t

	def predict_series(self, random = True):

		if random:
			T = np.linspace(0, self.settings.horizon, self.settings.n_steps)
			x = self.X0 * (1+self.growth_rate) ** T
			return x
		else:
			return self.x