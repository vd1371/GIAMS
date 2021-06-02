#Loading dependencies
import numpy as np

from .BaseSimulator import BaseSimulator
from utils.GeneralSettings import *

class EnvSimulator(BaseSimulator):

	def __init__(self, **params):
		super().__init__(**params)

		self.asset = params.pop('asset')
		self.random = True

	def reset(self):

		user_costs = 0
		elements_costs = np.zeros(self.settings.n_elements)
		elements_utils = np.zeros(self.settings.n_elements)
		elements_conds = np.zeros(self.settings.n_elements)
		elements_age = np.zeros(self.settings.n_elements)

		self.elements_conds_stepwise = [np.zeros(self.settings.n_steps, dtype = int) for _ in range(self.settings.n_elements)]

		# Generate hazards
		self.hazard = self.asset.hazard_model.generator.generate_one_lifecycle(horizon = self.settings.horizon,
																	dt = self.settings.dt)

		# Find the MRR costs to be used later, for each element in the horizon
		self.mrr_costs = []
		for element_idx, element in enumerate (self.asset.elements):
			self.mrr_costs.append(element.agency_cost_model.predict_series(self.random))

		# Refreshing the asset
		self.asset.refresh_age()

		self.step = 0

		for idx in range(self.settings.n_elements):
			elements_conds[idx] = self.asset.elements[idx].initial_condition
			elements_age[idx] = self.asset.elements[idx].age

		return {'step' : self.step,
			'deviation': 0,
			'user_costs' : user_costs,
			'elements_costs' : elements_costs,
			'elements_utils' : elements_utils,
			'elements_conds' : elements_conds,
			'elements_age' : elements_age,
			'done': self.step == (self.settings.n_steps - 1)
		}

	def cost_of(self, mrr, is_hazard = True):
		'''Getting the costs of actions for managing the budget in RL'''
		elements_costs = np.zeros(self.settings.n_elements)

		# Max duration will be used for the user cost
		max_duration = 0
		recovery_action = None

		for element_idx, element in enumerate (self.asset.elements):
			
			got_recovery = False
			# Finding the current condition, before taking any actions
			if self.step == 0:
				previous_condition = element.initial_condition
			else:
				previous_condition = self.elements_conds_stepwise[element_idx][self.step-1]

			# Finding the action
			action = mrr[element_idx]

			# The earthquake is missed because we don't know whether an earthquake will happen
			# or not...

			# If there is a planned MRR action
			if not action == DONOT:
				# Adding the agency costs
				elements_costs[element_idx] += self.mrr_costs[element_idx][action][self.step]

		return elements_costs, self.step

	def take_one_step(self, mrr, is_hazard = True):
		'''Get one instance of simulation in the life cycle'''
		user_costs = 0
		elements_costs = np.zeros(self.settings.n_elements)
		elements_utils = np.zeros(self.settings.n_elements)
		elements_conds = np.zeros(self.settings.n_elements)
		elements_age = np.zeros(self.settings.n_elements)
			
		# Max duration will be used for the user cost
		max_duration = 0
		recovery_action = None

		for element_idx, element in enumerate (self.asset.elements):
			
			got_recovery = False
			# Finding the current condition, before taking any actions
			if self.step == 0:
				previous_condition = element.initial_condition
			else:
				previous_condition = self.elements_conds_stepwise[element_idx][self.step-1]

			# Finding the action
			action = mrr[element_idx]

			# If there is an earthquake in that year, 
			iter_year = self.step*self.settings.dt
			if iter_year in self.hazard and is_hazard:
				after_hazard_condition, ds = self.asset.hazard_model.response.get(previous_condition = previous_condition,
																		pga = self.hazard[iter_year])
				
				# The earthquake has had severe effects and the state has changed
				if not after_hazard_condition == previous_condition:

					next_condition, recovery_action = self.asset.hazard_model.recovery.get(after_hazard_condition)
					
					if not recovery_action is DONOT:
						elements_costs[element_idx] += self.mrr_costs[element_idx][recovery_action][self.step]
						max_duration = max(max_duration, self.asset.mrr_model.mrr_duration[recovery_action])
						got_recovery = True

				# If it's the latest element
				if element_idx == self.settings.n_elements - 1:
					
					# Adding the loss cost of the asset due to earthquake
					user_costs += self.asset.hazard_model.loss.predict_series(ds, self.random)[self.step]
						
			# If the asset did not get recovery
			if not got_recovery:

				# If none of the above, then simple degradation
				if action == DONOT:
					next_condition = \
						element.deterioration_model.predict_condition(previous_condition = previous_condition,
																		age = element.age)
				# If there is a planned MRR action
				elif not action == DONOT:

					# Updating the max duration
					max_duration = max(max_duration, self.asset.mrr_model.mrr_duration[action])

					# Finding the next conidtion
					next_condition = self.asset.mrr_model.effectiveness.get(previous_condition, action)

					# Adding the agency costs
					elements_costs[element_idx] += self.mrr_costs[element_idx][action][self.step]

					# Adding the utility of the action on the element at the year
					elements_utils[element_idx] += element.utility_model.get(previous_condition,
																							next_condition)

			# If it's the latest element (This is done to ensure the user cost is added only once)
			if element_idx == self.settings.n_elements - 1:

				# Add the user cost to the asset_cost
				deviation = 1- (self.asset.user_cost_model.predict_series(1, True)[self.step]/ \
								self.asset.user_cost_model.predict_series(1, False)[self.step])

				user_costs += self.asset.user_cost_model.predict_series(max_duration, self.random)[self.step]

			# Updating the age of the element
			if action == RECON or recovery_action == RECON:
				element.set_age(0)
			else:
				element.add_age(self.settings.dt)

			# adding the condition to the element_condition_stepwise
			self.elements_conds_stepwise[element_idx][self.step] = next_condition
			elements_conds[element_idx] = next_condition

			elements_age[element_idx] = element.age

		self.step += 1

		return {'step' : self.step,
			'user_costs' : user_costs,
			'elements_costs' : elements_costs,
			'elements_utils' : elements_utils,
			'elements_conds' : elements_conds,
			'elements_age' : elements_age,
			'deviation': deviation,
			'done': self.step == (self.settings.n_steps - 1)
		}

