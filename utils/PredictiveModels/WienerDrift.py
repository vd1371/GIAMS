from .BasePredictiveModel import BasePredictiveModel
import numpy as np


class WienerDrift(BasePredictiveModel):

	def __init__(self, X0 = None, drift = None, volatility = None):
		super().__init__(X0 = X0)
		
		'''
		This is a simple linear predictor model
		f(t) = mt + c
		m : drift
		c : X0
		'''
		self.drift = drift
		self.volatility = volatility

	def predict(self, t = None):
		return self.predict_series(t)[t//self.dt]

	def predict_series(self):

		T = np.linspace(0, self.horizon, self.n_steps)
		W = np.random.standard_normal(size = self.n_steps) 
		W = np.cumsum(W)*np.sqrt(self.dt) ### standard brownian motion ###
		x = self.drift * T + self.volatility * W + self.X0
		return x


if __name__ == "__main__":

	import matplotlib.pyplot as plt

	mylin = WienerPredictor(drift = 2, volatility = 2, X0=5, dt = 2)
	vals = mylin.predict_series(20)
	

	import time
	start = time.time()
	i = 0
	while i < 100000:
		i += 1
		vals = mylin.predict_series(20)

	print (time.time()-start)