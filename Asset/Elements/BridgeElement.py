import numpy as np
from .BaseElement import BaseElement

class BridgeElement(BaseElement):

	def __init__(self, name = 'Deck', initial_condition = 0, age = 0, length = 0, width = 0, material= None):
		super().__init__(name, initial_condition, age)

		self.length = length
		self.width = width
		self.material = material
	