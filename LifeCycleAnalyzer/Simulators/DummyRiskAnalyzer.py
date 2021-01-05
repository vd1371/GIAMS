import numpy as np

from .BaseSimulator import BaseSimulator
from utils.GeneralSettings import *
import time

class DummyRiskAnalyzer(BaseSimulator):

	def __init__(self):
		super().__init__()

	def get_one_instance(self, asset, is_hazard = True, random = True):

		user_costs_stepwise = np.random.random(self.n_steps)
		elements_costs_stepwise = np.random.random(size = (self.n_steps, asset.n_elements)).tolist()
		elements_utils_stepwise = np.random.random(size = (self.n_steps, asset.n_elements)).tolist()
		elements_conds_stepwise = np.random.random(size = (self.n_steps, asset.n_elements)).tolist()

		return user_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise, elements_conds_stepwise
