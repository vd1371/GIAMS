from .BaseDistribution import BaseDistribution

class Exponential(BaseDistribution):

	def __init__(self, rate):
		super().__init__()
		self.rate = rate

	def set(self, rate):
		self.rate = rate

	def sample(self):
		# https://numpy.org/doc/stable/reference/random/generator.html?highlight=generator#numpy.random.Generator
		return self.generator.exponential(1/self.rate)