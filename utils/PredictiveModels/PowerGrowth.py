from .BasePredictiveModel import BasePredictiveModel
import numpy as np


class Power(BasePredictiveModel):

	def __init__(self, X0 = None, growth_rate = None):
		super().__init__(X0 = X0)
		
		'''
		This is a simple linear predictor model
		f(t) = mt + c
		m : drift
		c : X0
		'''
		self.growth_rate = growth_rate

	def predict(self, T = None):
		return self.X0 * (1+self.growth_rate) ** t

	def predict_series(self):
		T = np.linspace(0, self.horizon, self.n_steps)
		x = self.X0 * (1+self.growth_rate) ** T
		return x