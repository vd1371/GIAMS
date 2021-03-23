#Loading dependencies
from .BaseDistribution import BaseDistribution

class Exponential(BaseDistribution):

	def __init__(self, rate, scale = 0):
		super().__init__()
		self.rate = rate
		self.scale = scale

	def set(self, rate, scale = 0):
		self.rate = rate
		self.scale = scale

	def sample(self):
		# https://numpy.org/doc/stable/reference/random/generator.html?highlight=generator#numpy.random.Generator
		return self.scale + self.generator.exponential(1/self.rate)