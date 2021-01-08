# Loading dependencies
from .BasePredictiveModel import BasePredictiveModel
import numpy as np

class GBM(BasePredictiveModel):
	def __init__(self, **params):
		super().__init__(**params)
		'''Geometric brownian motion model

		::params::
		drift:
		volatility
		'''
		self.drift = params.pop('drift')
		self.volatility = params.pop('volatility')
		self.x = self.predict_series(random = True)

	def predict(self, t = None):
		return self.predict_series(t)[t//self.settings.dt]

	def predict_series(self, random = True):

		if random:

			T = np.linspace(0, self.settings.horizon, self.settings.n_steps)
			W = np.random.standard_normal(size = N) 
			W = np.cumsum(W)*np.sqrt(self.settings.dt) ### standard brownian motion ###
			x = (self.drift - 0.5*self.volatility**2)*T + self.volatility*W
			x = self.X0*np.exp(X)

			return x
		else:
			return self.x
