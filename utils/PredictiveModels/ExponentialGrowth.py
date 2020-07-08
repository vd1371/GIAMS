from .BasePredictiveModel import BasePredictiveModel
import numpy as np


class Exponential(BasePredictiveModel):

	def __init__(self, X0 = None, growth_rate = 0.04):
		super().__init__(X0 = X0)
		
		'''
		This is a simple linear predictor model
		f(t) = mt + c
		m : drift
		c : X0
		'''
		self.growth_rate = growth_rate

	def predict(self, t = None):
		return self.X0 * np.exp(t*self.growth_rate)

	def predict_series(self):
		T = np.linspace(0, self.horizon, self.n_steps)
		x = self.X0 * np.exp(T*self.growth_rate)
		return x