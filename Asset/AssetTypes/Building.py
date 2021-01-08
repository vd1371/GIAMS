'''
This is the main asset class
'''
import numpy as np
from utils.PredictiveModels.Linear import Linear

from .BaseAsset import BaseAsset

class Building(BaseAsset):

	def __init__(self, ID = 11111, **kwargs):
		super().__init__(ID, **kwargs)

	def set_seismic_info(self, structural_type = 'Steel',
								site_class = 'A'):
	
		self.structural_type = structural_type
		self.site_class = site_class

	def set_replacement_value_model(self, model = None):
		
		self.replacement_value = Linear(X0 = 100, drift = 0, settings = self.settings)

	