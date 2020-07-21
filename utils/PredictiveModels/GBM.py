from .BasePredictiveModel import BasePredictiveModel
import numpy as np

class GBM(BasePredictiveModel):
	def __init__(self, X0 = None, drift = None,  volatility= None):
		super().__init__(X0 = X0)
		
		'''
		This is a simple linear predictor model
		f(t) = mt + c
		m : slope
		c : intercept
		'''
		self.drift = drift
		self.volatility = volatility

		self.x = self.predict_series(random = True)

	def predict(self, t = None):
		return self.predict_series(t)[t//self.dt]

	def predict_series(self, random = True):

		if random:

			T = np.linspace(0, self.horizon, self.n_steps)
			W = np.random.standard_normal(size = N) 
			W = np.cumsum(W)*np.sqrt(self.dt) ### standard brownian motion ###
			x = (self.drift - 0.5*self.volatility**2)*T + self.volatility*W
			x = self.X0*np.exp(X)

			return vals
		else:
			return self.x
