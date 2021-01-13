#Loading dependencies
import numpy as np
import matplotlib.pyplot as plt

from .BaseSimulator import BaseSimulator
from utils.GeneralSettings import *
import time

class SHMSimulator(BaseSimulator):

	def __init__(self, **params):
		super().__init__(**params)

	def get_one_instance(self, asset, is_hazard = True, random = True):

		# In this dummy simulator for SHM, it is assumed that only 1 element is being
		# studied. Further modifications could lead to more advanced models.
		agency_costs = np.zeros(self.settings.n_steps)

		# Generate hazards
		hazard = asset.hazard_model.generator.generate_one_lifecycle(horizon = self.settings.horizon,
																	dt = self.settings.dt)
		# Finding an instance of replcement value in the horizon
		replacement_value = asset.replacement_value.predict_series(random)

		# Find the MRR costs to be used later, for each element in the horizon
		mrr_costs = []
		for element_idx, element in enumerate (asset.elements):
			mrr_costs.append(element.agency_cost_model.predict_series(random))

		# Refreshing the asset
		asset.refresh_age()

		mrr = asset.mrr_model.mrr_to_decimal()
		for step in range(self.settings.n_steps):
			
			# Max duration will be used for the user cost
			max_duration = 0
			recovery_action = None
			for element_idx, element in enumerate (asset.elements):
				
				got_recovery = False
				# Finding the current condition, before taking any actions
				if step == 0:
					previous_condition = element.initial_condition
				else:
					previous_condition = elements_conds_stepwise[element_idx][step-1]

				# Finding the action
				action = mrr[element_idx][step]

				# If there is an earthquake in that year, 
				iter_year = step*self.settings.dt
				if iter_year in hazard and is_hazard:
					after_hazard_condition, ds = asset.hazard_model.response.get(previous_condition = previous_condition,
																			pga = hazard[iter_year])
					
					# The earthquake has had severe effects and the state has changed
					if not after_hazard_condition == previous_condition:

						next_condition, recovery_action = asset.hazard_model.recovery.get(after_hazard_condition)
						
						if not recovery_action is DONOT:
							elements_costs_stepwise[element_idx][step] += mrr_costs[element_idx][recovery_action][step]
							max_duration = max(max_duration, asset.mrr_model.mrr_duration[recovery_action])
							got_recovery = True

					# If it's the latest element
					if element_idx == self.settings.n_elements - 1:
						
						# Adding the loss cost of the asset due to earthquake
						user_costs_stepwise[step] += asset.hazard_model.loss.predict_series(ds, random)[step]
							
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
						max_duration = max(max_duration, asset.mrr_model.mrr_duration[action])

						# Finding the next conidtion
						next_condition = asset.mrr_model.effectiveness.get(previous_condition, action)

						# Adding the agency costs
						elements_costs_stepwise[element_idx][step] += mrr_costs[element_idx][action][step]

						# Adding the utility of the action on the element at the year
						elements_utils_stepwise[element_idx][step] += element.utility_model.get(previous_condition,
																								next_condition)

				# If it's the latest element (This is done to ensure the user cost is added only once)
				if element_idx == self.settings.n_elements - 1:

					# Add the user cost to the asset_cost
					user_costs_stepwise[step] += asset.user_cost_model.predict_series(max_duration, random)[step]

				# Updating the age of the element
				if action == RECON or recovery_action == RECON:
					element.set_age(0)
				else:
					element.add_age(self.settings.dt)

				# adding the condition to the element_condition_stepwise
				elements_conds_stepwise[element_idx][step] = next_condition

		return user_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise, elements_conds_stepwise
