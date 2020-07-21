import numpy as np
import matplotlib.pyplot as plt
import pprint

from .BaseSimulator import BaseSimulator
from utils.GeneralSettings import *
import time

class BridgeSimulator(BaseSimulator):

	def __init__(self):
		super().__init__()

	def get_one_instance(self, asset, is_hazard = True, random = True):

		user_costs_stepwise = np.zeros(self.n_steps)
		elements_costs_stepwise = [np.zeros(self.n_steps) for _ in range(asset.n_elements)]
		elements_utils_stepwise = [np.zeros(self.n_steps) for _ in range(asset.n_elements)]

		# Generate hazards
		hazard = asset.hazard_model.generator.generate_one_lifecycle(horizon = self.horizon, dt = self.dt)

		# Finding an instance of replcement value in the horizon
		replacement_value = asset.replacement_value.predict_series(random, "replacement_value in simulator")

		# Find the MRR costs to be used later, for each element in the horizon
		mrr_costs = []
		for element_idx, element in enumerate (asset.elements):
			mrr_costs.append(element.agency_cost_model.predict_series(random))

		mrr = asset.mrr_model.mrr_to_decimal()
		for step in range(self.n_steps):

			# print (step, "Step counter in simulator")
			
			# Max duration will be used for the user cost
			max_duration = 0
			recovery_action = None
			for element_idx, element in enumerate (asset.elements):
				
				# Finding the current condition, before taking any actions
				previous_condition = element.initial_condition if step == 0 else element.conditions_in_horizon[step-1]

				# Finding the action
				action = mrr[element_idx][step]

				# If there is an earthquake in that year
				iter_year = step*self.dt
				if iter_year in hazard and is_hazard:
					next_condition, ds = asset.hazard_model.response.get(previous_condition = previous_condition, pga = hazard[iter_year])
					
					# The earthquake has had severe effects and the state has changes
					if not next_condition == previous_condition:

						next_condition, recovery_action = asset.hazard_model.recovery.get(next_condition)
						
						if not recovery_action is self.DONOT:
							elements_costs_stepwise[element_idx][step] += mrr_costs[element_idx][recovery_action][step]
							max_duration = max(max_duration, asset.mrr_model.mrr_duration[recovery_action])

					# If it's the latest element
					if element_idx == self.n_elements - 1:
						
						# Adding the loss cost of the asset due to earthquake
						user_costs_stepwise[step] += asset.hazard_model.loss.predict_series(ds, random)[step]

					# print ('next_condition', next_condition, 'in hazard. Element_idx:', element_idx)
							
				# If there is a planned MRR action
				else:
					if not action == self.DONOT:

						# Updating the max duration
						max_duration = max(max_duration, asset.mrr_model.mrr_duration[action])

						# Finding the next conidtion
						next_condition = asset.mrr_model.effectiveness.get(previous_condition, action)

						# Adding the agency costs
						elements_costs_stepwise[element_idx][step] += mrr_costs[element_idx][action][step]

						# Adding the utility of the action on the element at the year
						elements_utils_stepwise[element_idx][step] += element.utility_model.get(previous_condition, next_condition)

						# print ('next_condition', next_condition, 'in mrr. Element_idx:', element_idx)

					# If none of the above, then simple degradation
					elif action == self.DONOT:
						next_condition = element.deterioration_model.predict_condition(previous_condition = previous_condition, age = element.age)

						# print ('next_condition', next_condition, 'in deterioration. Element_idx:', element_idx)

				# If it's the latest element (This is done to ensure the user cost is added only once)
				if element_idx == self.n_elements - 1:

					# Add the user cost to the asset_cost
					user_costs_stepwise[step] += asset.user_cost_model.predict_series(max_duration, random)[step]

				# Updating the age of the element
				if action == self.RECON or recovery_action == self.RECON:
					element.set_age(0)
				else:
					element.add_age(self.dt)

				element.append_next_condition(next_condition)

		return user_costs_stepwise, elements_costs_stepwise, elements_utils_stepwise
