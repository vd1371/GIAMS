#Loading dependencies
import numpy as np

from .BaseSimulator import BaseSimulator
from utils.GeneralSettings import *

class DummyRiskAnalyzer(BaseSimulator):

	def __init__(self):
		super().__init__()

	def get_one_instance(self, asset, is_hazard = True, random = True):
		'''Get one instance of simulation in the life cycle'''
		user_costs_stepwise = np.random.random(self.settings.n_steps)
		elements_costs_stepwise = np.random.random(size = (self.settings.n_elements, self.settings.n_steps)).tolist()
		elements_risk_stepwise = np.random.random(size = (self.settings.n_elements, self.settings.n_steps)).tolist()
		elements_conds_stepwise = np.random.random(size = (self.settings.n_elements, self.settings.n_steps)).tolist()

		return user_costs_stepwise, elements_costs_stepwise, elements_risk_stepwise, elements_conds_stepwise
