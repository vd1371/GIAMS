#Loading dependencies
import numpy as np
from .BaseMRREffectiveness import *
from utils.GeneralSettings import *

class SHMEffectiveness(BaseMRREffectiveness):
	
	def __init__(self, **params):
		super().__init__(**params)
		'''Dummy effectiveness for the whole SHM analysis
		
		The output of SHM actions are solely random
		'''

	def get(self, previous_state, action):
		'''A dummy effectiveness model for  the SHM example'''
		effectiveness_dict = {INSP1 : [0, 1],
								INSP2: [0, 1],
								DOMNT: [0, 1]}
		return np.random.choice(effectiveness_dict[action])