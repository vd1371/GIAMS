# Loading dependencies
from .BasePredictiveModel import BasePredictiveModel
import numpy as np

class Linear(BasePredictiveModel):
	def __init__(self, **params):
		super().__init__(**params)
		'''Linear predictie model for the future trends
		
		This is a simple linear predictor model
		f(t) = mt + c
		m : drift
		c : X0
		'''
		self.drift = params.pop('drift')
		self.x = self.predict_series(random = True)

	def predict(self, t = None):
		return self.drift * t + self.X0

	def predict_series(self, random = True, *args):

		if random:
			T = np.linspace(0, self.settings.horizon, self.settings.n_steps)
			x = self.drift * T + self.X0
			return x
		else:
			return self.x