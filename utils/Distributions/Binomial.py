#Loading dependencies
from .BaseDistribution import BaseDistribution

class Binomial(BaseDistribution):

	def __init__(self, n, p):
		super().__init__()
		self.n = n
		self.p = p

	def set(self, n, p):
		self.n = n
		self.p = p

	def sample(self):
		# https://numpy.org/doc/stable/reference/random/generator.html?highlight=generator#numpy.random.Generator
		return self.generator.binomial(self.n, self.p)