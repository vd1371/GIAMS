#Loading dependencies
from .BaseDistribution import BaseDistribution

class Normal(BaseDistribution):

	def __init__(self, mu, sigma):
		super().__init__()
		self.mu = mu
		self.sigma = sigma

	def set(self, mu, sigma):
		self.mu = mu
		self.sigma = sigma

	def sample(self):
		# https://numpy.org/doc/stable/reference/random/generator.html?highlight=generator#numpy.random.Generator
		return self.generator.normal(self.mu, self.sigma)