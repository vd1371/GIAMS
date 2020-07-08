from .BasePredictiveModel import BasePredictiveModel
import numpy as np


class Linear(BasePredictiveModel):

	def __init__(self, X0 = None, drift = None):
		super().__init__(X0 = X0)
		
		'''
		This is a simple linear predictor model
		f(t) = mt + c
		m : drift
		c : X0
		'''
		self.drift = drift

	def predict(self, t = None):
		return self.drift * t + self.X0

	def predict_series(self):
		T = np.linspace(0, self.horizon, self.n_steps)
		x = self.drift * T + self.X0
		return x