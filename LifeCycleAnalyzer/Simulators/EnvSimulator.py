#Loading dependencies
import numpy as np

from .BaseSimulator import BaseSimulator
from utils.GeneralSettings import *

class EnvSimulator(BaseSimulator):

	def __init__(self, **params):
		super().__init__(**params)

	def simulate(self, asset,
						model,
						eps,
						is_hazard = True,
						random = True):
		'''Get one instance of simulation in the life cycle'''
		user_costs_stepwise = np.zeros(self.settings.n_steps)
		elements_costs_stepwise = [np.zeros(self.settings.n_steps) for _ in range(self.settings.n_elements)]
		elements_utils_stepwise = [np.zeros(self.settings.n_steps) for _ in range(self.settings.n_elements)]
		elements_conds_stepwise = [np.zeros(self.settings.n_steps, dtype = int) for _ in range(self.settings.n_elements)]

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

		for step in range(self.settings.n_steps):
			
			# Max duration will be used for the user cost
			max_duration = 0
			recovery_action = None

			# Deciding what should be done based on the decision model
			mrr = model.predict_action()

			for element_idx, element in enumerate (asset.elements):
				
				got_recovery = False
				# Finding the current condition, before taking any actions
				if step == 0:
					previous_condition = element.initial_condition
				else:
					previous_condition = elements_conds_stepwise[element_idx][step-1]

				# Finding the action
				action = mrr[element_idx]

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
