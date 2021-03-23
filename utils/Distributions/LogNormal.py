#Loading dependencies
from .BaseDistribution import BaseDistribution

class LogNormal(BaseDistribution):

	'''
	mean: float or array_like of floats, optional
	Mean value of the underlying normal distribution. Default is 0.

	sigma: float or array_like of floats, optional
	Standard deviation of the underlying normal distribution. Must be non-negative. Default is 1.
	'''

	def __init__(self, mu, sigma):
		super().__init__()
		self.mu = mu
		self.sigma = sigma

	def set(self, mu, sigma):
		self.mu = mu
		self.sigma = sigma

	def sample(self):
		# https://numpy.org/doc/stable/reference/random/generator.html?highlight=generator#numpy.random.Generator
		return self.generator.lognormal(self.mu, self.sigma)